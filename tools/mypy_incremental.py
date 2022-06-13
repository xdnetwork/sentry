import configparser
import os
import sys

BASE_SETTINGS = (
    ("python_version", "3.8"),
    ("mypy_path", "src:."),
    ("files", "src,fixtures,tools,tests"),
    ("show_error_codes", "true"),
    # mypy settings
    ("check_untyped_defs", "true"),
    # TODO: once done with incremental types flip this
    ("follow_imports", "silent"),
    # TODO: can we turn these on?
    # ('disallow_any_generics', 'true'),
    # ('disallow_incomplete_defs', 'true'),
    # ('no_implicit_optional', 'true'),
    ("warn_redundant_casts", "true"),
    ("warn_unused_configs", "true"),
    # ('warn_unused_ignores', 'true'),
)

STRICT_SETTINGS = (
    ("disallow_any_generics", "true"),
    ("disallow_subclassing_any", "true"),
    ("disallow_untyped_calls", "true"),
    ("disallow_untyped_defs", "true"),
    ("disallow_incomplete_defs", "true"),
    # ('check_untyped_defs', 'true'), inherited
    ("disallow_untyped_decorators", "true"),
    ("no_implicit_optional", "true"),
    ("warn_unused_ignores", "true"),
    ("warn_return_any", "true"),
    ("no_implicit_reexport", "true"),
    ("strict_equality", "true"),
)

THIRD_PARTY_UNTYPED = (
    "amqp",
    "boto3",
    "botocore",
    "brotli",
    "bs4",
    "celery",
    "confluent_kafka",
    "django",
    "django_zero_downtime_migrations",
    "docker",
    "email_reply_parser",
    "exam",
    "fido2",
    "google",
    "honcho",
    "isodate",
    "jsonschema",
    "kombu",
    "lxml",
    "mistune",
    "mmh3",
    "msgpack",
    "onelogin",
    "openapi_core",
    "parsimonious",
    "petname",
    "phabricator",
    "picklefield",
    "progressbar",
    "pytest_benchmark",
    "pytest_rerunfailures",
    "rapidjson",
    "rb",
    "rediscluster",
    "requests_oauthlib",
    "rest_framework",
    "sentry_relay",
    "sqlparse",
    "statsd",
    "symbolic",
    "toronado",
    "ua_parser",
    "u2flib_server",
    "unidiff",
    "uwsgi",
    "uwsgidecorators",
    "zstandard",
)

STRICT_MODULES = (
    "sentry.analytics",
    "sentry.api.bases.external_actor",
    "sentry.api.bases.organization_events",
    "sentry.api.bases.rule",
    "sentry.api.endpoints.codeowners",
    "sentry.api.endpoints.organization_events_stats",
    "sentry.api.endpoints.organization_events_trace",
    "sentry.api.endpoints.project_app_store_connect_credentials",
    "sentry.api.endpoints.team_issue_breakdown",
    "sentry.api.endpoints.team_unresolved_issue_age",
    "sentry.api.helpers.group_index",
    "sentry.api.serializers.base",
    "sentry.api.serializers.models.external_actor",
    "sentry.api.serializers.models.integration",
    "sentry.api.serializers.models.notification_setting",
    "sentry.api.serializers.models.organization",
    "sentry.api.serializers.models.organization_member",
    "sentry.api.serializers.models.team",
    "sentry.api.serializers.models.user",
    "sentry.api.serializers.types",
    "sentry.api.validators.external_actor",
    "sentry.api.validators.notifications",
    "sentry.apidocs",
    "sentry.constants",
    "sentry.db.models.base",
    "sentry.db.models.fields.bounded",
    "sentry.db.models.fields.foreignkey",
    "sentry.db.models.fields.onetoone",
    "sentry.db.models.fields.text",
    "sentry.db.models.manager",
    "sentry.db.models.paranoia",
    "sentry.db.models.query",
    "sentry.db.models.utils",
    "sentry.digests",
    "sentry.features",
    "sentry.grouping.result",
    "sentry.grouping.strategies.base",
    "sentry.grouping.strategies.legacy",
    "sentry.grouping.strategies.message",
    "sentry.grouping.strategies.newstyle",
    "sentry.grouping.strategies.security",
    "sentry.grouping.strategies.template",
    "sentry.grouping.strategies.utils",
    "sentry.incidents.charts",
    "sentry.integrations.base",
    "sentry.integrations.github",
    "sentry.integrations.slack",
    "sentry.integrations.vsts",
    "sentry.killswitches",
    "sentry.lang.native.appconnect",
    "sentry.mail.notifications",
    "sentry.models.debugfile",
    "sentry.models.groupsubscription",
    "sentry.models.options",
    "sentry.models.rulefirehistory",
    "sentry.notifications",
    "sentry.ownership.grammar",
    "sentry.pipeline",
    "sentry.processing.realtime_metrics",
    "sentry.profiles",
    "sentry.ratelimits",
    "sentry.relay.config.metric_extraction",
    "sentry.release_health",
    "sentry.roles.manager",
    "sentry.rules",
    "sentry.search.base",
    "sentry.search.events.builder",
    "sentry.search.events.constants",
    "sentry.search.events.types",
    "sentry.search.snuba",
    "sentry.sentry_metrics",
    "sentry.shared_integrations",
    "sentry.snuba.entity_subscription",
    "sentry.snuba.outcomes",
    "sentry.snuba.query_subscription_consumer",
    "sentry.snuba.metrics.fields.histogram",
    "sentry.snuba.metrics.fields.base",
    "sentry.snuba.metrics.naming_layer",
    "sentry.snuba.metrics.query",
    "sentry.spans",
    "sentry.tasks.app_store_connect",
    "sentry.tasks.low_priority_symbolication",
    "sentry.tasks.store",
    "sentry.tasks.symbolication",
    "sentry.tasks.update_user_reports",
    "sentry.unmerge",
    "sentry.utils.appleconnect",
    "sentry.utils.avatar",
    "sentry.utils.codecs",
    "sentry.utils.committers",
    "sentry.utils.cursors",
    "sentry.utils.dates",
    "sentry.utils.email",
    "sentry.utils.event_frames",
    "sentry.utils.jwt",
    "sentry.utils.kvstore",
    "sentry.utils.outcomes",
    "sentry.utils.patch_set",
    "sentry.utils.services",
    "sentry.utils.time_window",
    "sentry.web.decorators",
    "tests.sentry.lang.native.test_appconnect",
    "tests.sentry.processing.realtime_metrics",
    "tests.sentry.tasks.test_low_priority_symbolication",
    "tests.sentry.utils.appleconnect",
    "tools",
)


def main() -> int:
    cfg = configparser.ConfigParser()

    cfg.add_section("mypy")
    for k, v in BASE_SETTINGS:
        cfg.set("mypy", k, v)

    for mod in STRICT_MODULES:
        section = f"mypy-{mod}.*"
        cfg.add_section(section)
        for k, v in STRICT_SETTINGS:
            cfg.set(section, k, v)

    for mod in THIRD_PARTY_UNTYPED:
        section = f"mypy-{mod}.*"
        cfg.add_section(section)
        cfg.set(section, "ignore_missing_imports", "true")

    with open("mypy.ini", "w") as f:
        cfg.write(f)

    cmd = (sys.executable, "-m", "mypy", *sys.argv[1:])
    os.execvp(cmd[0], cmd)


if __name__ == "__main__":
    raise SystemExit(main())
