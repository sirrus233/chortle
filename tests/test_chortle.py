import os

import boto3
import pytest
from chortle.lambda_function import lambda_handler
from moto import mock_dynamodb2

TEST_SERIAL = "0000000000000000"
TEST_EVENT = {
    "serialNumber": TEST_SERIAL,
    "clickType": "SINGLE",
    "batteryVoltage": "1337mV",
}


@pytest.fixture(scope="function")
def table():
    with mock_dynamodb2():
        os.environ["CHORTLE_DYNAMO_TABLE"] = "test-table"
        yield boto3.resource("dynamodb", region_name="us-west-2").create_table(
            TableName=os.environ["CHORTLE_DYNAMO_TABLE"],
            AttributeDefinitions=[
                {"AttributeName": "button_serial", "AttributeType": "S"},
                {"AttributeName": "click_type", "AttributeType": "S"},
            ],
            KeySchema=[
                {"AttributeName": "button_serial", "KeyType": "HASH"},
                {"AttributeName": "click_type", "KeyType": "RANGE"},
            ],
        )


def _put_item(
    table,
    strategy,
    button_serial=TEST_SERIAL,
    click_type="SINGLE",
    active=True,
    chore="test-chore",
    last_pressed_time=0,
    reset_time_seconds=0,
    dependent=None,
):
    item = {
        "button_serial": button_serial,
        "click_type": click_type,
        "active": active,
        "chore": chore,
        "last_pressed_time": last_pressed_time,
        "reset_time_seconds": reset_time_seconds,
        "strategy": strategy,
    }
    if dependent:
        item["dependent"] = dependent

    table.put_item(Item=item)


def test_periodic_strategy(table):
    _put_item(table, "PERIODIC")
    lambda_handler(TEST_EVENT, None)
    response = table.get_item(
        Key={"button_serial": TEST_SERIAL, "click_type": "SINGLE"}
    )
    item = response["Item"]
    assert item["last_pressed_time"] > 0


@pytest.mark.parametrize("starting_active_state", [False, True])
def test_toggle_strategy(table, starting_active_state):
    _put_item(table, "TOGGLE", active=starting_active_state)
    lambda_handler(TEST_EVENT, None)
    response = table.get_item(
        Key={"button_serial": TEST_SERIAL, "click_type": "SINGLE"}
    )
    item = response["Item"]
    assert item["last_pressed_time"] > 0
    assert item["active"] != starting_active_state


def test_modal_toggle_strategy(table):
    dependent_serial = f"{TEST_SERIAL[:-1]}1"
    _put_item(
        table, "MODAL_TOGGLE", active=False, dependent=[dependent_serial, "SINGLE"],
    )
    _put_item(table, "TOGGLE", active=True, button_serial=dependent_serial)
    lambda_handler(TEST_EVENT, None)
    response = table.get_item(
        Key={"button_serial": dependent_serial, "click_type": "SINGLE"}
    )
    dependent = response["Item"]
    response = table.get_item(
        Key={"button_serial": TEST_SERIAL, "click_type": "SINGLE"}
    )
    item = response["Item"]
    assert item["last_pressed_time"] > 0
    assert not dependent["active"]
    assert item["active"]


def test_unknown_strategies_handled(table):
    _put_item(table, "Fake-strategy")
    lambda_handler(TEST_EVENT, None)
    assert True
