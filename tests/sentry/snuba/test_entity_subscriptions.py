import pytest
from snuba_sdk import And, Column, Condition, Function, Op

from sentry.exceptions import (
    InvalidQuerySubscription,
    InvalidSearchQuery,
    UnsupportedQuerySubscription,
)
from sentry.search.events.constants import METRICS_MAP
from sentry.sentry_metrics import indexer
from sentry.sentry_metrics.configuration import UseCaseKey
from sentry.sentry_metrics.utils import resolve, resolve_tag_key
from sentry.snuba.dataset import EntityKey
from sentry.snuba.entity_subscription import (
    EventsEntitySubscription,
    MetricsCountersEntitySubscription,
    MetricsSetsEntitySubscription,
    PerformanceMetricsEntitySubscription,
    PerformanceTransactionsEntitySubscription,
    SessionsEntitySubscription,
    get_entity_key_from_snuba_query,
    get_entity_subscription,
    get_entity_subscription_from_snuba_query,
)
from sentry.snuba.metrics.naming_layer.mri import SessionMRI
from sentry.snuba.models import QueryDatasets, SnubaQuery
from sentry.testutils import TestCase


class EntitySubscriptionTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()
        for tag in [
            SessionMRI.SESSION.value,
            SessionMRI.USER.value,
            "session.status",
            "init",
            "crashed",
        ]:
            indexer.record(
                use_case_id=UseCaseKey.RELEASE_HEALTH, org_id=self.organization.id, string=tag
            )

    def test_get_entity_subscriptions_for_sessions_dataset_non_supported_aggregate(self) -> None:
        aggregate = "count(sessions)"
        with pytest.raises(UnsupportedQuerySubscription):
            get_entity_subscription(
                query_type=SnubaQuery.Type.CRASH_RATE,
                dataset=QueryDatasets.SESSIONS,
                aggregate=aggregate,
                time_window=3600,
                extra_fields={"org_id": self.organization.id},
            )

    def test_get_entity_subscriptions_for_sessions_dataset_missing_organization(self) -> None:
        aggregate = "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate"
        with pytest.raises(InvalidQuerySubscription):
            get_entity_subscription(
                query_type=SnubaQuery.Type.CRASH_RATE,
                dataset=QueryDatasets.SESSIONS,
                aggregate=aggregate,
                time_window=3600,
            )

    def test_build_query_builder_invalid_fields_raise_error(self) -> None:
        entities = [
            get_entity_subscription(
                query_type=SnubaQuery.Type.CRASH_RATE,
                dataset=QueryDatasets.SESSIONS,
                aggregate="percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate",
                time_window=3600,
                extra_fields={"org_id": self.organization.id},
            ),
            get_entity_subscription(
                query_type=SnubaQuery.Type.ERROR,
                dataset=QueryDatasets.EVENTS,
                aggregate="count_unique(user)",
                time_window=3600,
            ),
        ]
        for entity in entities:
            with pytest.raises(InvalidSearchQuery, match="Invalid key for this search: timestamp"):
                entity.build_query_builder("timestamp:-24h", [self.project.id], None)

    def test_get_entity_subscriptions_for_sessions_dataset(self) -> None:
        aggregate = "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate"
        entity_subscription = get_entity_subscription(
            query_type=SnubaQuery.Type.CRASH_RATE,
            dataset=QueryDatasets.SESSIONS,
            aggregate=aggregate,
            time_window=3600,
            extra_fields={"org_id": self.organization.id},
        )
        assert isinstance(entity_subscription, SessionsEntitySubscription)
        assert entity_subscription.aggregate == aggregate
        assert entity_subscription.get_entity_extra_params() == {
            "organization": self.organization.id
        }
        assert entity_subscription.dataset == QueryDatasets.SESSIONS
        snql_query = entity_subscription.build_query_builder(
            "", [self.project.id], None
        ).get_snql_query()
        snql_query.query.select.sort(key=lambda q: q.function)
        assert snql_query.query.select == [
            Function(
                function="identity", parameters=[Column(name="sessions")], alias="_total_count"
            ),
            Function(
                function="if",
                parameters=[
                    Function(function="greater", parameters=[Column(name="sessions"), 0]),
                    Function(
                        function="divide",
                        parameters=[Column(name="sessions_crashed"), Column(name="sessions")],
                    ),
                    None,
                ],
                alias="_crash_rate_alert_aggregate",
            ),
        ]
        assert snql_query.query.where == [
            Condition(Column(name="project_id"), Op.IN, [self.project.id]),
            Condition(Column(name="org_id"), Op.EQ, None),
        ]

    def test_get_entity_subscription_for_metrics_dataset_non_supported_aggregate(self) -> None:
        aggregate = "count(sessions)"
        with pytest.raises(UnsupportedQuerySubscription):
            get_entity_subscription(
                query_type=SnubaQuery.Type.CRASH_RATE,
                dataset=QueryDatasets.METRICS,
                aggregate=aggregate,
                time_window=3600,
                extra_fields={"org_id": self.organization.id},
            )

    def test_get_entity_subscription_for_metrics_dataset_missing_organization(self) -> None:
        aggregate = "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate"
        with pytest.raises(InvalidQuerySubscription):
            get_entity_subscription(
                query_type=SnubaQuery.Type.CRASH_RATE,
                dataset=QueryDatasets.METRICS,
                aggregate=aggregate,
                time_window=3600,
            )

    def test_get_entity_subscription_for_metrics_dataset_for_users(self) -> None:
        org_id = self.organization.id
        use_case_id = UseCaseKey.RELEASE_HEALTH

        aggregate = "percentage(users_crashed, users) AS _crash_rate_alert_aggregate"
        entity_subscription = get_entity_subscription(
            query_type=SnubaQuery.Type.CRASH_RATE,
            dataset=QueryDatasets.METRICS,
            aggregate=aggregate,
            time_window=3600,
            extra_fields={"org_id": self.organization.id},
        )
        assert isinstance(entity_subscription, MetricsSetsEntitySubscription)
        assert entity_subscription.aggregate == aggregate
        assert entity_subscription.get_entity_extra_params() == {
            "organization": self.organization.id,
            "granularity": 10,
        }
        assert entity_subscription.dataset == QueryDatasets.METRICS
        session_status = resolve_tag_key(use_case_id, org_id, "session.status")
        session_status_crashed = resolve(use_case_id, org_id, "crashed")
        snql_query = entity_subscription.build_query_builder(
            "", [self.project.id], None, {"organization_id": self.organization.id}
        ).get_snql_query()
        key = lambda func: func.alias
        assert sorted(snql_query.query.select, key=key) == sorted(
            [
                Function("uniq", parameters=[Column("value")], alias="count"),
                Function(
                    "uniqIf",
                    parameters=[
                        Column(name="value"),
                        Function(
                            function="equals",
                            parameters=[
                                Column(session_status),
                                session_status_crashed,
                            ],
                        ),
                    ],
                    alias="crashed",
                ),
            ],
            key=key,
        )
        assert snql_query.query.where == [
            Condition(Column("project_id"), Op.IN, [self.project.id]),
            Condition(Column("org_id"), Op.EQ, self.organization.id),
            Condition(
                Column("metric_id"),
                Op.EQ,
                resolve(
                    UseCaseKey.RELEASE_HEALTH,
                    self.organization.id,
                    entity_subscription.metric_key.value,
                ),
            ),
        ]

    def test_get_entity_subscription_for_metrics_dataset_for_sessions(self) -> None:
        org_id = self.organization.id
        use_case_id = UseCaseKey.RELEASE_HEALTH
        aggregate = "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate"
        entity_subscription = get_entity_subscription(
            query_type=SnubaQuery.Type.CRASH_RATE,
            dataset=QueryDatasets.METRICS,
            aggregate=aggregate,
            time_window=3600,
            extra_fields={"org_id": self.organization.id},
        )
        assert isinstance(entity_subscription, MetricsCountersEntitySubscription)
        assert entity_subscription.aggregate == aggregate
        assert entity_subscription.get_entity_extra_params() == {
            "organization": self.organization.id,
            "granularity": 10,
        }
        assert entity_subscription.dataset == QueryDatasets.METRICS
        session_status = resolve_tag_key(use_case_id, org_id, "session.status")
        session_status_crashed = resolve(use_case_id, org_id, "crashed")
        session_status_init = resolve(use_case_id, org_id, "init")
        snql_query = entity_subscription.build_query_builder(
            "", [self.project.id], None, {"organization_id": self.organization.id}
        ).get_snql_query()
        key = lambda func: func.alias
        assert sorted(snql_query.query.select, key=key) == sorted(
            [
                Function(
                    function="sumIf",
                    parameters=[
                        Column("value"),
                        Function(
                            "equals", parameters=[Column(session_status), session_status_init]
                        ),
                    ],
                    alias="count",
                ),
                Function(
                    "sumIf",
                    parameters=[
                        Column(name="value"),
                        Function(
                            "equals", parameters=[Column(session_status), session_status_crashed]
                        ),
                    ],
                    alias="crashed",
                ),
            ],
            key=key,
        )
        assert snql_query.query.where == [
            Condition(Column("project_id"), Op.IN, [self.project.id]),
            Condition(Column("org_id"), Op.EQ, self.organization.id),
            Condition(
                Column("metric_id"),
                Op.EQ,
                resolve(use_case_id, self.organization.id, entity_subscription.metric_key.value),
            ),
            Condition(
                Column(session_status),
                Op.IN,
                [session_status_crashed, session_status_init],
            ),
        ]

    def test_get_entity_subscription_for_performance_transactions_dataset(self) -> None:
        aggregate = "percentile(transaction.duration,.95)"
        entity_subscription = get_entity_subscription(
            query_type=SnubaQuery.Type.PERFORMANCE,
            dataset=QueryDatasets.TRANSACTIONS,
            aggregate=aggregate,
            time_window=3600,
        )
        assert isinstance(entity_subscription, PerformanceTransactionsEntitySubscription)
        assert entity_subscription.aggregate == aggregate
        assert entity_subscription.get_entity_extra_params() == {}
        assert entity_subscription.dataset == QueryDatasets.TRANSACTIONS
        snql_query = entity_subscription.build_query_builder(
            "", [self.project.id], None
        ).get_snql_query()
        assert snql_query.query.select == [
            Function(
                "quantile(0.95)",
                parameters=[Column(name="duration")],
                alias="percentile_transaction_duration__95",
            )
        ]
        assert snql_query.query.where == [Condition(Column("project_id"), Op.IN, [self.project.id])]

    def test_get_entity_subscription_for_performance_metrics_dataset(self) -> None:
        aggregate = "percentile(transaction.duration,.95)"
        entity_subscription = get_entity_subscription(
            query_type=SnubaQuery.Type.PERFORMANCE,
            dataset=QueryDatasets.METRICS,
            aggregate=aggregate,
            time_window=3600,
            extra_fields={"org_id": self.organization.id},
        )
        assert isinstance(entity_subscription, PerformanceMetricsEntitySubscription)
        assert entity_subscription.aggregate == aggregate
        assert entity_subscription.get_entity_extra_params() == {
            "organization": self.organization.id,
            "granularity": 60,
        }
        assert entity_subscription.dataset == QueryDatasets.PERFORMANCE_METRICS
        snql_query = entity_subscription.build_query_builder(
            "",
            [self.project.id],
            None,
            {
                "organization_id": self.organization.id,
            },
        ).get_snql_query()

        metric_id = resolve(
            UseCaseKey.PERFORMANCE, self.organization.id, METRICS_MAP["transaction.duration"]
        )

        assert snql_query.query.select == [
            Function(
                function="arrayElement",
                parameters=[
                    Function(
                        function="quantilesIf(0.95)",
                        parameters=[
                            Column(name="value"),
                            Function(
                                function="equals",
                                parameters=[Column(name="metric_id"), metric_id],
                            ),
                        ],
                    ),
                    1,
                ],
                alias="percentile_transaction_duration__95",
            )
        ]
        assert snql_query.query.where == [
            Condition(Column("project_id"), Op.IN, [self.project.id]),
            Condition(Column("org_id"), Op.EQ, self.organization.id),
            Condition(Column("metric_id"), Op.IN, [metric_id]),
        ]

    def test_get_entity_subscription_for_events_dataset(self) -> None:
        aggregate = "count_unique(user)"
        entity_subscription = get_entity_subscription(
            query_type=SnubaQuery.Type.ERROR,
            dataset=QueryDatasets.EVENTS,
            aggregate=aggregate,
            time_window=3600,
        )
        assert isinstance(entity_subscription, EventsEntitySubscription)
        assert entity_subscription.aggregate == aggregate
        assert entity_subscription.get_entity_extra_params() == {}
        assert entity_subscription.dataset == QueryDatasets.EVENTS

        snql_query = entity_subscription.build_query_builder(
            "release:latest", [self.project.id], None
        ).get_snql_query()
        assert snql_query.query.select == [
            Function(
                function="uniq",
                parameters=[Column(name="tags[sentry:user]")],
                alias="count_unique_user",
            )
        ]
        assert snql_query.query.where == [
            And(
                [
                    Condition(Column("type"), Op.EQ, "error"),
                    Condition(
                        Function(
                            function="ifNull", parameters=[Column(name="tags[sentry:release]"), ""]
                        ),
                        Op.IN,
                        [],
                    ),
                ]
            ),
            Condition(Column("project_id"), Op.IN, [self.project.id]),
        ]


class GetEntitySubscriptionFromSnubaQueryTest(TestCase):
    def test(self):
        cases = [
            (EventsEntitySubscription, SnubaQuery.Type.ERROR, QueryDatasets.EVENTS, "count()"),
            (
                PerformanceTransactionsEntitySubscription,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.TRANSACTIONS,
                "count()",
            ),
            (
                PerformanceMetricsEntitySubscription,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.METRICS,
                "count()",
            ),
            (
                PerformanceMetricsEntitySubscription,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.PERFORMANCE_METRICS,
                "count()",
            ),
            (
                PerformanceMetricsEntitySubscription,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.METRICS,
                "count_unique(user)",
            ),
            (
                PerformanceMetricsEntitySubscription,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.PERFORMANCE_METRICS,
                "count_unique(user)",
            ),
            (
                MetricsCountersEntitySubscription,
                SnubaQuery.Type.CRASH_RATE,
                QueryDatasets.METRICS,
                "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate",
            ),
            (
                MetricsSetsEntitySubscription,
                SnubaQuery.Type.CRASH_RATE,
                QueryDatasets.METRICS,
                "percentage(users_crashed, users) AS _crash_rate_alert_aggregate",
            ),
        ]

        for expected_entity_subscription, query_type, dataset, aggregate in cases:
            snuba_query = SnubaQuery(
                time_window=60,
                type=query_type.value,
                dataset=dataset.value,
                aggregate=aggregate,
            )
            assert isinstance(
                get_entity_subscription_from_snuba_query(snuba_query, self.organization.id),
                expected_entity_subscription,
            )


class GetEntityKeyFromSnubaQueryTest(TestCase):
    def test(self):
        cases = [
            (EntityKey.Events, SnubaQuery.Type.ERROR, QueryDatasets.EVENTS, "count()", ""),
            (
                EntityKey.Transactions,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.TRANSACTIONS,
                "count()",
                "",
            ),
            (
                EntityKey.GenericMetricsDistributions,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.METRICS,
                "count()",
                "",
            ),
            (
                EntityKey.GenericMetricsSets,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.METRICS,
                "count_unique(user)",
                "",
            ),
            (
                EntityKey.GenericMetricsDistributions,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.PERFORMANCE_METRICS,
                "count()",
                "",
            ),
            (
                EntityKey.GenericMetricsSets,
                SnubaQuery.Type.PERFORMANCE,
                QueryDatasets.PERFORMANCE_METRICS,
                "count_unique(user)",
                "",
            ),
            (
                EntityKey.MetricsCounters,
                SnubaQuery.Type.CRASH_RATE,
                QueryDatasets.METRICS,
                "percentage(sessions_crashed, sessions) AS _crash_rate_alert_aggregate",
                "",
            ),
            (
                EntityKey.MetricsSets,
                SnubaQuery.Type.CRASH_RATE,
                QueryDatasets.METRICS,
                "percentage(users_crashed, users) AS _crash_rate_alert_aggregate",
                "",
            ),
        ]

        for expected_entity_key, query_type, dataset, aggregate, query in cases:
            snuba_query = SnubaQuery(
                time_window=60,
                type=query_type.value,
                dataset=dataset.value,
                aggregate=aggregate,
                query=query,
            )
            assert expected_entity_key == get_entity_key_from_snuba_query(
                snuba_query, self.organization.id, self.project.id
            )
