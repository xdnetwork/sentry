from datetime import timedelta

from sentry.snuba.models import QueryDatasets, SnubaQuery, SnubaQueryEventType
from sentry.snuba.subscriptions import create_snuba_query
from sentry.testutils import TestCase


class SnubaQueryEventTypesTest(TestCase):
    def test(self):
        snuba_query = create_snuba_query(
            SnubaQuery.Type.ERROR,
            QueryDatasets.EVENTS,
            "release:123",
            "count()",
            timedelta(minutes=10),
            timedelta(minutes=1),
            None,
            [SnubaQueryEventType.EventType.DEFAULT, SnubaQueryEventType.EventType.ERROR],
        )
        assert set(snuba_query.event_types) == {
            SnubaQueryEventType.EventType.DEFAULT,
            SnubaQueryEventType.EventType.ERROR,
        }
