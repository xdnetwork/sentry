from snuba_sdk.query import Query

from sentry.snuba.metrics.query import MetricsQuery

# Tags -> Column("tags[transaction]")
# Function team_key_transactions


def tranform_mqb_query_to_metrics_query(query: Query) -> MetricsQuery:
    ...
