"""Definitions of chore handling strategies

Every chore in Chortle has a boolean active state, and a strategy that determines how
the state should respond to an event. An inactive chore is always shown as "green",
indicating that no work needs to be done. An active chore may show as "green" or "red",
depending on the strategy and the last time an event was received.

Each strategy method in this module has documentation describing how it affects its
chore.
"""
import time
from typing import Any, Dict, List, Tuple

TableEntry = Dict[str, Any]
TableKey = Dict[str, str]
TableExpr = str
TableExprAttrs = Dict[str, Any]
UpdateExpression = Tuple[TableKey, TableExpr, TableExprAttrs]


def update_entry_time(entry: TableEntry) -> UpdateExpression:
    """Construct a dynamo expression that will update the "last pressed time" for a chore.

    :param entry: TableEntry for this chore.
    :return: Expression to update the last pressed time in the table.
    """
    current_time = int(time.time())
    key = {"button_serial": entry["button_serial"], "click_type": entry["click_type"]}
    expr = "SET last_pressed_time=:t"
    expr_attrs = {":t": current_time}
    return key, expr, expr_attrs


def get_periodic_update_expression(entry: TableEntry) -> List[UpdateExpression]:
    """Create an update expression for the PERIODIC strategy. This strategy is used for
    chores that should be performed at least once per given time interval. The chore
    is always considered active, and a chore event needs only to update when the chore
    was last performed.

    Example chore: Cleaning the cat box. This must be done 1/day, and cleaning the box
    resets the 24 hour timer.

    :param entry: TableEntry for this chore.
    :return: List of update expressions for dynamo.
    """
    update_expression = update_entry_time(entry)
    return [update_expression]


def get_toggle_update_expression(entry: TableEntry) -> List[UpdateExpression]:
    """Create an update expression for the TOGGLE strategy. This strategy is used for
    chores that need to be manually scheduled, and then marked as done (optionally
    after a timeout). The chore is considered inactive until an event arrives, and then
    remains active until it receives another event.

    Example chore: Emptying the dishwasher. This becomes an active chore when the
    dishwasher is started and the timer starts. After the dishwasher runs, the timer has
    run out, and the chore goes red until a second toggle deactivates it.

    :param entry: TableEntry for this chore.
    :return: List of update expressions for dynamo.
    """
    key, expr, expr_attrs = update_entry_time(entry)
    expr += ", active=:a"
    expr_attrs[":a"] = not entry["active"]
    update_expression = (key, expr, expr_attrs)
    return [update_expression]


def get_modal_toggle_update_expression(entry: TableEntry) -> List[UpdateExpression]:
    """Create an update expression for the MODAL_TOGGLE strategy. This strategy is used
    for toggleable chores (see the TOGGLE strategy) that should automatically disable
    some dependent toggleable chore upon receiving an enabling event.

    Example chore: Moving laundry from dryer to hamper. The dependent chore (which uses
    the TOGGLE strategy) is moving laundry from washer to dryer. The washer to dryer
    chore is toggled on when the washer starts. Instead of toggling it off after the
    timeout (wash cycle duration), the dryer to hamper chore is toggled. This MODAL
    chore has its own timeout (dryer cycle duration), and also automatically deactivates
    the washer to dryer chore.

    :param entry: TableEntry for this chore.
    :return: List of update expressions for dynamo.
    """
    parent_update_expression = get_toggle_update_expression(entry)
    dependent_update_expression = []
    # Only update the dependent chore if this chore was inactive and is now
    # toggling to active.
    if not entry["active"]:
        dependent_key = {
            "button_serial": entry["dependent"][0],
            "click_type": entry["dependent"][1],
        }
        dependent_expr = "SET active=:a"
        dependent_expr_attrs = {":a": False}
        dependent_update_expression.append(
            (dependent_key, dependent_expr, dependent_expr_attrs)
        )
    return parent_update_expression + dependent_update_expression


STRATEGY_FUNCTIONS = {
    "PERIODIC": get_periodic_update_expression,
    "TOGGLE": get_toggle_update_expression,
    "MODAL_TOGGLE": get_modal_toggle_update_expression,
}


def get_update_expression(entry: TableEntry) -> List[UpdateExpression]:
    """Given a TableEntry representing a single chore, execute the strategy for that
    chore.

    :param entry: TableEntry for the chore.
    :return: List of dynamo update expressions resulting from the chosen strategy.
    """
    strategy = entry["strategy"]
    if strategy not in STRATEGY_FUNCTIONS:
        print(f"Unknown strategy: {strategy}")
        return []
    return STRATEGY_FUNCTIONS[strategy](entry)
