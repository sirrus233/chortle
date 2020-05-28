import os
from dataclasses import asdict

import pytest
from chortle.build import Chore, build_chortle_table, create_table
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
        os.environ["CHORTLE_DYNAMO_TABLE"] = "chortle"
        yield create_table()


@mock_dynamodb2
def test_build_table():
    build_chortle_table()


def test_periodic_strategy(table):
    table.put_item(Item=asdict(Chore(button_serial=TEST_SERIAL, strategy="PERIODIC")))
    lambda_handler(TEST_EVENT, None)
    response = table.get_item(
        Key={"button_serial": TEST_SERIAL, "click_type": "SINGLE"}
    )
    item = response["Item"]
    assert item["last_pressed_time"] > 0


@pytest.mark.parametrize("initial_state", [False, True])
def test_toggle_strategy(table, initial_state):
    table.put_item(
        Item=asdict(
            Chore(button_serial=TEST_SERIAL, strategy="TOGGLE", active=initial_state)
        )
    )
    lambda_handler(TEST_EVENT, None)
    response = table.get_item(
        Key={"button_serial": TEST_SERIAL, "click_type": "SINGLE"}
    )
    item = response["Item"]
    assert item["last_pressed_time"] > 0
    assert item["active"] != initial_state


def test_modal_toggle_strategy(table):
    dependent_serial = f"{TEST_SERIAL[:-1]}1"
    table.put_item(
        Item=asdict(
            Chore(
                button_serial=TEST_SERIAL,
                strategy="MODAL_TOGGLE",
                active=False,
                dependent=[dependent_serial, "SINGLE"],
            )
        )
    )
    table.put_item(
        Item=asdict(
            Chore(button_serial=dependent_serial, strategy="TOGGLE", active=True)
        )
    )
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
    table.put_item(
        Item=asdict(Chore(button_serial=TEST_SERIAL, strategy="fake-strategy"))
    )
    lambda_handler(TEST_EVENT, None)
    assert True
