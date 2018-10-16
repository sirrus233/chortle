import time


class UnknownStrategyException(Exception):
    pass


def __get_periodic_update_expression(entry):
    current_time = int(time.time())
    expr = 'SET last_pressed_time=:t'
    expr_attrs = {':t': current_time}
    return expr, expr_attrs


def __get_toggle_update_expression(entry):
    current_time = int(time.time())
    active = not entry['active']
    expr = 'SET last_pressed_time=:t, active=:a'
    expr_attrs = {':t': current_time, ':a': active}
    return expr, expr_attrs


def __get_modal_update_expression(entry):
    current_time = int(time.time())
    expr = 'SET last_pressed_time=:t'
    expr_attrs = {':t': current_time}
    return expr, expr_attrs


STRATEGY_FUNCTIONS = {
    'PERIODIC': __get_periodic_update_expression,
    'TOGGLE':   __get_toggle_update_expression,
    'MODAL':    __get_modal_update_expression
}


def get_update_expression(entry):
    strategy = entry['strategy']
    if strategy in STRATEGY_FUNCTIONS:
        return STRATEGY_FUNCTIONS[strategy](entry)
    else:
        raise UnknownStrategyException()
