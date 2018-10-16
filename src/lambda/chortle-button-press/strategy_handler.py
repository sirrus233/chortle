import time


class UnknownStrategyException(Exception):
    pass


def __update_entry_time(entry):
    current_time = int(time.time())
    key = {'button_serial': entry['button_serial'], 'click_type': entry['click_type']}
    expr = 'SET last_pressed_time=:t'
    expr_attrs = {':t': current_time}
    return key, expr, expr_attrs


def __get_periodic_update_expression(entry):
    update_expression = __update_entry_time(entry)
    return [update_expression]


def __get_toggle_update_expression(entry):
    key, expr, expr_attrs = __update_entry_time(entry)
    expr += ', active=:a'
    expr_attrs[':a'] = not entry['active']
    update_expression = (key, expr, expr_attrs)
    return [update_expression]


def __get_modal_toggle_update_expression(entry):
    parent_update_expression = __get_toggle_update_expression(entry)
    dependent_update_expression = []
    # Only update the dependent chore if this chore was inactive and is now toggling to active
    if not entry['active']:
        dependent_key = {'button_serial': entry['dependent'][0], 'click_type': entry['dependent'][1]}
        dependent_expr = 'SET active=:a'
        dependent_expr_attrs = {':a': False}
        dependent_update_expression.append((dependent_key, dependent_expr, dependent_expr_attrs))
    return parent_update_expression + dependent_update_expression


STRATEGY_FUNCTIONS = {
    'PERIODIC': __get_periodic_update_expression,
    'TOGGLE':   __get_toggle_update_expression,
    'MODAL_TOGGLE':    __get_modal_toggle_update_expression
}


def get_update_expression(entry):
    strategy = entry['strategy']
    if strategy in STRATEGY_FUNCTIONS:
        return STRATEGY_FUNCTIONS[strategy](entry)
    else:
        raise UnknownStrategyException()
