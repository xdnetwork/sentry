import logging
from datetime import timedelta
from urllib.parse import urlparse

from django.utils import timezone

from sentry import options
from sentry.auth.access import get_cached_organization_member
from sentry.auth.superuser import is_active_superuser
from sentry.models import OrganizationMember
from sentry.search.utils import InvalidQuery, parse_datetime_string
from sentry.utils.dates import parse_stats_period

logger = logging.getLogger(__name__)

MAX_STATS_PERIOD = timedelta(days=90)


class InvalidParams(Exception):
    pass


def get_datetime_from_stats_period(stats_period, now=None):
    if now is None:
        now = timezone.now()
    parsed_stats_period = parse_stats_period(stats_period)
    if parsed_stats_period is None:
        raise InvalidParams(f"Invalid statsPeriod: {stats_period!r}")
    try:
        return now - parsed_stats_period
    except OverflowError:
        raise InvalidParams(f"Invalid statsPeriod: {stats_period!r}")


def default_start_end_dates(now=None, default_stats_period=MAX_STATS_PERIOD):
    if now is None:
        now = timezone.now()
    return now - default_stats_period, now


def get_date_range_from_params(params, optional=False, default_stats_period=MAX_STATS_PERIOD):
    """
    Gets a date range from standard date range params we pass to the api.

    If `statsPeriod` is passed then convert to a time delta and make sure it
    fits within our min/max period length. Values are in the format
    <number><period_type>, where period type is one of `s` (seconds),
    `m` (minutes), `h` (hours) or `d` (days).

    Similarly, `statsPeriodStart` and `statsPeriodEnd` allow for selecting a
    relative range, for example: 15 days ago through 8 days ago. This uses the same
    format as `statsPeriod`

    :param params:
    If `start` end `end` are passed, validate them, convert to `datetime` and
    returns them if valid.
    :param optional: When True, if no params passed then return `(None, None)`.
    :param default_stats_period: When set, this becomes the interval upon which default start and
    and end dates are defined
    :return: A length 2 tuple containing start/end or raises an `InvalidParams`
    exception
    """
    now = timezone.now()

    start, end = default_start_end_dates(now, default_stats_period)

    stats_period = params.get("statsPeriod")
    stats_period_start = params.get("statsPeriodStart")
    stats_period_end = params.get("statsPeriodEnd")

    if stats_period is not None:
        start = get_datetime_from_stats_period(stats_period, now)

    elif stats_period_start or stats_period_end:
        if not all([stats_period_start, stats_period_end]):
            raise InvalidParams("statsPeriodStart and statsPeriodEnd are both required")
        start = get_datetime_from_stats_period(stats_period_start, now)
        end = get_datetime_from_stats_period(stats_period_end, now)

    elif params.get("start") or params.get("end"):
        if not all([params.get("start"), params.get("end")]):
            raise InvalidParams("start and end are both required")
        try:
            start = parse_datetime_string(params["start"])
            end = parse_datetime_string(params["end"])
        except InvalidQuery as e:
            raise InvalidParams(str(e))
    elif optional:
        return None, None

    if start >= end:
        raise InvalidParams("start must be before end")

    return start, end


def is_member_disabled_from_limit(request, organization):
    user = request.user

    # never limit sentry apps
    if getattr(user, "is_sentry_app", False):
        return False

    # don't limit super users
    if is_active_superuser(request):
        return False

    # must be a simple user at this point
    try:
        member = get_cached_organization_member(user.id, organization.id)
    except OrganizationMember.DoesNotExist:
        # if org member doesn't exist, we should be getting an auth error later
        return False
    else:
        return member.flags["member-limit:restricted"]


def generate_organization_hostname(org_slug: str) -> str:
    url_prefix_hostname = urlparse(options.get("system.url-prefix")).netloc
    org_base_hostname_template = options.get("system.organization-base-hostname")
    if not org_base_hostname_template:
        return url_prefix_hostname
    if "{slug}" not in org_base_hostname_template or "{region}" not in org_base_hostname_template:
        return url_prefix_hostname
    org_hostname = org_base_hostname_template.replace("{slug}", org_slug)
    region = options.get("system.region") or None
    if region is None:
        return url_prefix_hostname
    org_hostname = org_hostname.replace("{region}", region)
    return org_hostname


def generate_organization_url(org_slug: str) -> str:
    org_url_template = options.get("system.organization-url-template")
    if not org_url_template:
        return options.get("system.url-prefix")
    return org_url_template.replace("{hostname}", generate_organization_hostname(org_slug))
