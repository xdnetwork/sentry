from sentry.incidents.models import AlertRuleTriggerAction
from sentry.snuba.models import QueryDatasets, SnubaQuery, SnubaQueryEventType

__all__ = (
    "AlertRuleSerializer",
    "AlertRuleTriggerSerializer",
    "AlertRuleTriggerActionSerializer",
    "ACTION_TARGET_TYPE_TO_STRING",
    "STRING_TO_ACTION_TARGET_TYPE",
    "STRING_TO_ACTION_TYPE",
)

STRING_TO_ACTION_TYPE = {
    registration.slug: registration.type
    for registration in AlertRuleTriggerAction.get_registered_types()
}
ACTION_TARGET_TYPE_TO_STRING = {
    AlertRuleTriggerAction.TargetType.USER: "user",
    AlertRuleTriggerAction.TargetType.TEAM: "team",
    AlertRuleTriggerAction.TargetType.SPECIFIC: "specific",
    AlertRuleTriggerAction.TargetType.SENTRY_APP: "sentry_app",
}
STRING_TO_ACTION_TARGET_TYPE = {v: k for (k, v) in ACTION_TARGET_TYPE_TO_STRING.items()}
QUERY_TYPE_VALID_EVENT_TYPES = {
    SnubaQuery.Type.ERROR: {
        SnubaQueryEventType.EventType.ERROR,
        SnubaQueryEventType.EventType.DEFAULT,
    },
    SnubaQuery.Type.PERFORMANCE: {SnubaQueryEventType.EventType.TRANSACTION},
}
QUERY_TYPE_VALID_DATASETS = {
    SnubaQuery.Type.ERROR: {QueryDatasets.EVENTS},
    SnubaQuery.Type.PERFORMANCE: {QueryDatasets.TRANSACTIONS, QueryDatasets.PERFORMANCE_METRICS},
    SnubaQuery.Type.CRASH_RATE: {QueryDatasets.METRICS, QueryDatasets.SESSIONS},
}

# TODO(davidenwang): eventually we should pass some form of these to the event_search parser to raise an error
UNSUPPORTED_QUERIES = {"release:latest"}

# Allowed time windows (in minutes) for crash rate alerts
CRASH_RATE_ALERTS_ALLOWED_TIME_WINDOWS = [30, 60, 120, 240, 720, 1440]


from .alert_rule import AlertRuleSerializer
from .alert_rule_trigger import AlertRuleTriggerSerializer
from .alert_rule_trigger_action import AlertRuleTriggerActionSerializer
