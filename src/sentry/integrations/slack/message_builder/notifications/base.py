from __future__ import annotations

from typing import Any, Mapping

from sentry.integrations.slack.message_builder import SlackBody
from sentry.integrations.slack.message_builder.base.base import URL_FORMAT_STR, SlackMessageBuilder
from sentry.models import Team, User
from sentry.notifications.notifications.base import BaseNotification
from sentry.types.integrations import ExternalProviders
from sentry.utils import json


class SlackNotificationsMessageBuilder(SlackMessageBuilder):
    def __init__(
        self,
        notification: BaseNotification,
        context: Mapping[str, Any],
        recipient: Team | User,
    ) -> None:
        super().__init__()
        self.notification = notification
        self.context = context
        self.recipient = recipient

    def build(self) -> SlackBody:
        callback_id_raw = self.notification.get_callback_data()
        return self._build(
            title=self.notification.build_attachment_title(self.recipient),
            title_link=self.notification.get_title_link(self.recipient),
            text=self.notification.get_message_description(self.recipient),
            footer=self.notification.build_notification_footer(
                recipient=self.recipient,
                provider=ExternalProviders.SLACK,
                url_format_str=URL_FORMAT_STR,
            ),
            actions=self.notification.get_message_actions(self.recipient),
            callback_id=json.dumps(callback_id_raw) if callback_id_raw else None,
        )
