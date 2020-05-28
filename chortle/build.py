"""This module contains functions to create, initialize, and persist Chortle's AWS
resources. If these resources are ever lost or corrupted, this allows them to be
recreated from their initial state.
"""
from dataclasses import asdict, dataclass
from typing import List, Optional

import boto3
from mypy_boto3_dynamodb.service_resource import Table


@dataclass(frozen=True)
class Chore:
    """Define the parameters of a chore to be stored in the database"""

    button_serial: str = "0000"
    click_type: str = "SINGLE"
    strategy: str = "TOGGLE"
    chore_name: str = "chore-name"
    active: bool = True
    reset_time_seconds: int = 0
    dependent: Optional[List[str]] = None


def build_chortle_table() -> None:
    """Construct a new instance of the Chortle database, populate it, and upload."""
    table = create_table()

    chores = [
        Chore(
            button_serial="G030JF0520662DJS",
            click_type="SINGLE",
            strategy="PERIODIC",
            chore_name="Scoop Litter Box",
            reset_time_seconds=86400,
        ),
        Chore(
            button_serial="G030JF0520662DJS",
            click_type="DOUBLE",
            strategy="TOGGLE",
            chore_name="Empty the Dishwasher",
            reset_time_seconds=7800,
        ),
        Chore(
            button_serial="G030JF0520662DJS",
            click_type="LONG",
            strategy="TOGGLE",
            chore_name="Laundry: Washer to Dryer",
            reset_time_seconds=2400,
        ),
        Chore(
            button_serial="G030JF052373W8GP",
            click_type="SINGLE",
            strategy="MODAL_TOGGLE",
            chore_name="Laundry: Dryer to Hamper",
            reset_time_seconds=3600,
            dependent=["G030JF052373W8GP", "LONG"],
        ),
    ]

    for chore in chores:
        table.put_item(Item=asdict(chore))


def create_table() -> Table:
    """Creates an empty Chortle table in DynamoDB.
    :return: The DynamoDB table.
    """
    table_name = "chortle"
    client = boto3.client("dynamodb")
    client.create_table(
        TableName=table_name,
        AttributeDefinitions=[
            {"AttributeName": "button_serial", "AttributeType": "S"},
            {"AttributeName": "click_type", "AttributeType": "S"},
        ],
        KeySchema=[
            {"AttributeName": "button_serial", "KeyType": "HASH"},
            {"AttributeName": "click_type", "KeyType": "RANGE"},
        ],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    waiter = client.get_waiter("table_exists")
    waiter.wait(TableName=table_name, WaiterConfig={"Delay": 1})

    return boto3.resource("dynamodb").Table(table_name)
