import pytz
import datetime

from snuba_sdk.aliased_expression import AliasedExpression
from snuba_sdk.column import Column
from snuba_sdk.conditions import And, BooleanCondition, Condition, Op, Or
from snuba_sdk.entity import Entity
from snuba_sdk.expressions import Granularity, Limit, Offset
from snuba_sdk.function import CurriedFunction, Function
from snuba_sdk.orderby import Direction, LimitBy, OrderBy
from snuba_sdk.query import Query


TABLE_QUERIES = [
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p50",
                initializers=None,
                parameters=[
                    Column("transaction.duration")
                ],
                alias="p50",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            )
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 33, 21219, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 33, 21219, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[2],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=2,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                    function="p50",
                    initializers=None,
                    parameters=[
                        "transaction.duration"
                    ],
                    alias="p50",
                ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_sets"),
        "select": [
            Function(
                function="count_unique",
                initializers=None,
                parameters=[
                    Column("transaction.user"),
                ],
                alias="count_unique_user",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            )
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 33, 21219, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 33, 21219, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[2],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=2,
            ),
            Condition(
                lhs=Function(
                    function="tuple",
                    initializers=None,
                    parameters=[
                        Column("transaction")
                    ],
                    alias=None,
                ),
                op=Op.IN,
                rhs=Function(
                    function="tuple", initializers=None, parameters=[(12,), (17,)], alias=None
                ),
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p50",
                initializers=None,
                parameters=[
                    Column("transaction.duration")
                ],
                alias="p50_transaction_duration",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
        ],
        "groupby": [
            Column("project_id"),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 34, 26663, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 34, 26663, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[5],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=5,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p50",
                initializers=None,
                parameters=[
                    Column("transaction.duration")
                ],
                alias="p50_transaction_duration",
            ),
        ],
        "groupby": [
            Column("project_id"),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 34, 303387, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 34, 303387, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[6],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=6,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="count_web_vitals_measurements",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.lcp"),
                    "good"
                ],
                alias="count_web_vitals_measurements_cls_good",
            ),
            Function(
                function="count_web_vitals_measurements",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.fid"),
                    "meh"
                ],
                alias="count_web_vitals_measurements_fid_meh",
            ),
            Function(
                function="count_web_vitals_measurements",
                initializers=None,
                parameters=[
                    Column("transactions.measurements.fp"),
                    "good"
                ],
                alias="count_web_vitals_measurements_fp_good",
            ),
            Function(
                function="count_web_vitals_measurements",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.lcp"),
                    "good"
                ],
                alias="count_web_vitals_measurements_lcp_good",
            ),
            Function(
                function="count_web_vitals_measurements",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.fcp"),
                    "meh"
                ],
                alias="count_web_vitals_measurements_fcp_meh",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            )
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 35, 447729, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 35, 447729, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[11],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=11,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="count_web_vitals_measurements",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.lcp"),
                    "poor"
                ],
                alias="count_web_vitals_measurements_lcp_poor",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            )
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 35, 707018, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 35, 707018, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[12],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=12,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    Column("transaction.duration")
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="toInt8", initializers=None, parameters=[0], alias="team_key_transaction"
            ),
            AliasedExpression(exp=Column("transaction"), alias="transaction"),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 36, 75132, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 36, 75132, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[13],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=14,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p50",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p50",
            )
        ],
        "groupby": [],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 36, 936975, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 36, 936975, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[17],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=18,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=101),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="apdex",
                initializers=None,
                parameters=[],
                alias="apdex",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.cls"),
                ],
                alias="p75_measurements_cls",
            ),
            Function(
                function="divide",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="tpm",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.fid")
                ],
                alias="p75_measurements_fid",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.fcp")
                ],
                alias="p75_measurements_fcp",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.lcp")
                ],
                alias="p75_measurements_lcp",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 37, 278535, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 37, 278535, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[18],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=19,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_sets"),
        "select": [
            Function(
                function="count_unique",
                initializers=None,
                parameters=[
                    Column("transaction.user"),
                ],
                alias="count_unique_user",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Function(
                function="transaction.miserable_user",
                initializers=None,
                parameters=[],
                alias="count_miserable_user",
            ),
            Function(
                function="user_misery",
                initializers=None,
                parameters=[],
                alias="user_misery",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 37, 278535, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 37, 278535, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[18],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=19,
            ),
            Condition(
                lhs=Function(
                    function="tuple",
                    initializers=None,
                    parameters=[
                        Column("transaction"),
                        Column("project_id"),
                    ],
                    alias=None,
                ),
                op=Op.IN,
                rhs=Function(
                    function="tuple", initializers=None, parameters=[(437, "bar")], alias=None
                ),
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="apdex",
                initializers=None,
                parameters=[],
                alias="apdex",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.cls")
                ],
                alias="p75_measurements_cls",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="tpm",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.fid")
                ],
                alias="p75_measurements_fid",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.fcp")
                ],
                alias="p75_measurements_fcp",
            ),
            Function(
                function="p75",
                initializers=None,
                parameters=[
                    Column("transaction.measurements.lcp")
                ],
                alias="p75_measurements_lcp",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 37, 440461, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 37, 440461, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[18],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=19,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_sets"),
        "select": [
            Function(
                function="count_unique",
                initializers=None,
                parameters=[
                    Column("transaction.user"),
                ],
                alias="count_unique_user",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Function(
                function="transaction.miserable_user",
                initializers=None,
                parameters=[],
                alias="count_miserable_user",
            ),
            Function(
                function="user_misery",
                initializers=None,
                parameters=[],
                alias="user_misery",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id")
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 37, 440461, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 37, 440461, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[18],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=19,
            ),
            Condition(
                lhs=Function(
                    function="tuple",
                    initializers=None,
                    parameters=[
                        Column("transaction"),
                        Column("project_id")
                    ],
                    alias=None,
                ),
                op=Op.IN,
                rhs=Function(
                    function="tuple", initializers=None, parameters=[(437, 18)], alias=None
                ),
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="epm",
            ),
            AliasedExpression(
                exp=Column("environment"),
                alias="environment",
            ),
        ],
        "groupby": [
            Column("project_id"),
            AliasedExpression(
                exp=Column("environment"),
                alias="environment",
            ),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 37, 719279, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 37, 719279, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[19],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=20,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction"),
                    ),
                    [(20, 487)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 38, 32475, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 38, 32475, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[20],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=21,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(20, 487)],
                    ],
                    alias="team_key_transaction",
                ),
                direction=Direction.ASC,
            ),
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            ),
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction"),
                    ),
                    [(20, 487)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 38, 127281, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 38, 127281, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[20],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=21,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(20, 487)],
                    ],
                    alias="team_key_transaction",
                ),
                direction=Direction.ASC,
            ),
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            ),
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000,
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction"),
                    ),
                    [(21, 508), (21, 512)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 38, 458313, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 38, 458313, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[21],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=22,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(21, 508), (21, 512)],
                    ],
                    alias="team_key_transaction",
                ),
                direction=Direction.ASC,
            ),
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            ),
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction")
                    ),
                    [(21, 508), (21, 512)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 38, 552260, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 38, 552260, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[21],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=22,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(21, 508), (21, 512)],
                    ],
                    alias="team_key_transaction",
                ),
                direction=Direction.DESC,
            ),
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            ),
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction")
                    ),
                    [(22, 533), (22, 537)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(22, 533), (22, 537)],
                    ],
                    alias="team_key_transaction",
                ),
                op=Op.NEQ,
                rhs=0,
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 38, 893701, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 38, 893701, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[22],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=23,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction")
                    ),
                    [(22, 533), (22, 537)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(22, 533), (22, 537)],
                    ],
                    alias="team_key_transaction",
                ),
                op=Op.EQ,
                rhs=1,
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 38, 987457, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 38, 987457, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[22],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=23,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction")
                    ),
                    [(22, 533), (22, 537)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(22, 533), (22, 537)],
                    ],
                    alias="team_key_transaction",
                ),
                op=Op.EQ,
                rhs=0,
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 39, 77835, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 39, 77835, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[22],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=23,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction")
                    ),
                    [(22, 533), (22, 537)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Function(
                    function="in",
                    initializers=None,
                    parameters=[
                        (
                            Column(name="project_id", entity=None, subscriptable=None, key=None),
                            Column("transaction"),
                        ),
                        [(22, 533), (22, 537)],
                    ],
                    alias="team_key_transaction",
                ),
                op=Op.EQ,
                rhs=0,
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 39, 170133, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 39, 170133, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[22],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=23,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            Function(
                function="p50",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p50",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction"),
                alias="title",
            )
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 39, 419992, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 39, 419992, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[23],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=24,
            ),
        ],
        "having": [],
        "orderby": [],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
    {
        "match": Entity("metrics_distributions"),
        "select": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
            Function(
                function="rate",
                initializers=None,
                parameters=[
                    Column("transaction.duration"),
                    60,
                    7776000.0,
                ],
                alias="epm",
            ),
            Function(
                function="failure_rate",
                initializers=None,
                parameters=[],
                alias="failure_rate",
            ),
        ],
        "groupby": [
            AliasedExpression(
                exp=Column("transaction.status"),
                alias="transaction.status",
            ),
            Function(
                function="in",
                initializers=None,
                parameters=[
                    (
                        Column(name="project_id", entity=None, subscriptable=None, key=None),
                        Column("transaction")
                    ),
                    [(24, 592)],
                ],
                alias="team_key_transaction",
            ),
            AliasedExpression(
                exp=Column("transaction"),
                alias="transaction",
            ),
            Column("project_id"),
        ],
        "array_join": None,
        "where": [
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.GTE,
                rhs=datetime.datetime(2022, 3, 24, 11, 11, 39, 719119, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="timestamp", entity=None, subscriptable=None, key=None),
                op=Op.LT,
                rhs=datetime.datetime(2022, 6, 22, 11, 11, 39, 719119, tzinfo=pytz.utc),
            ),
            Condition(
                lhs=Column(name="project_id", entity=None, subscriptable=None, key=None),
                op=Op.IN,
                rhs=[24],
            ),
            Condition(
                lhs=Column(name="org_id", entity=None, subscriptable=None, key=None),
                op=Op.EQ,
                rhs=25,
            ),
        ],
        "having": [],
        "orderby": [
            OrderBy(
                exp=Function(
                function="p95",
                initializers=None,
                parameters=[
                    "transaction.duration"
                ],
                alias="p95",
            ),
                direction=Direction.ASC,
            )
        ],
        "limitby": None,
        "limit": Limit(limit=51),
        "offset": Offset(offset=0),
        "granularity": None,
        "totals": None,
    },
]