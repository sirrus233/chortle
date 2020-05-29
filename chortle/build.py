"""This module contains functions to create, initialize, and persist Chortle's AWS
resources. If these resources are ever lost or corrupted, this allows them to be
recreated from their initial state.
"""
from dataclasses import asdict, dataclass
from tempfile import SpooledTemporaryFile
from typing import List, Optional
from zipfile import ZipFile

import boto3
from mypy_boto3_dynamodb.service_resource import Table

TABLE_NAME = "chortle"
LAMBDA_FUNCTION_NAME = "chortle-button-press"


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

    # Example chores to start off the database
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
    client = boto3.client("dynamodb")
    client.create_table(
        TableName=TABLE_NAME,
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
    waiter.wait(TableName=TABLE_NAME, WaiterConfig={"Delay": 1})

    return boto3.resource("dynamodb").Table(TABLE_NAME)


def update_lambda() -> None:
    """Updates the Chortle lambda function with the latest code in this repository."""
    client = boto3.client("lambda", "us-west-2")

    with SpooledTemporaryFile() as payload:
        with ZipFile(payload, "w") as zipfile:
            zipfile.write("chortle/__init__.py")
            zipfile.write("chortle/lambda_function.py")
            zipfile.write("chortle/strategy_handler.py")

        payload.seek(0)

        client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME, ZipFile=payload.read()
        )

    client.update_function_configuration(
        FunctionName=LAMBDA_FUNCTION_NAME,
        Environment={"Variables": {"CHORTLE_DYNAMO_TABLE": TABLE_NAME}},
    )
