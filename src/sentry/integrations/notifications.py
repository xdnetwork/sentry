from __future__ import annotations

from abc import ABC
from typing import Any, Mapping, Union

from sentry.models import Event, Group, Team, User
from sentry.notifications.notifications.base import BaseNotification
from sentry.types.integrations import ExternalProviders

NotificationBody = Any


class AbstractMessageBuilder(ABC):
    pass


class NotificationMessageBuilderMixin:
    def __init__(
        self,
        notification: BaseNotification,
        context: Mapping[str, Any],
        recipient: Union[Team, User],
    ) -> None:
        super().__init__()
        self.notification = notification
        self.context = context
        self.recipient = recipient

    def build_attachment_title(self, group: Group | Event) -> str:
        ev_metadata = group.get_event_metadata()
        ev_type = group.get_event_type()

        if ev_type == "error" and "type" in ev_metadata:
            title = ev_metadata["type"]

        elif ev_type == "csp":
            title = f'{ev_metadata["directive"]} - {ev_metadata["uri"]}'

        else:
            title = group.title

        # Explicitly typing to satisfy mypy.
        title_str: str = title
        return title_str

    def get_title_link(
        self,
        group: Group,
        event: Event | None,
        link_to_event: bool,
        issue_details: bool,
        notification: BaseNotification | None,
    ) -> str:
        if event and link_to_event:
            url = group.get_absolute_url(params={"referrer": "slack"}, event_id=event.event_id)

        elif issue_details and notification:
            referrer = notification.get_referrer(ExternalProviders.SLACK)
            url = group.get_absolute_url(params={"referrer": referrer})

        else:
            url = group.get_absolute_url(params={"referrer": "slack"})

        # Explicitly typing to satisfy mypy.
        url_str: str = url
        return url_str
