"""Module defining the top level lambda function that receives all incoming Chortle
events.
"""
import os
from typing import Any, Dict

import boto3

from .strategy_handler import get_update_expression


def lambda_handler(event: Dict[str, str], _: Any) -> None:
    """
    Triggered whenever this lambda function receives an event, such as from an IoT
    button press.

    :param event: Event data as a dictionary. Button events carry the button's serial
     number, click type, and battery voltage.
    :param _: LambdaContext. See:
     https://docs.aws.amazon.com/lambda/latest/dg/python-context.html
    :return: None
    """
    # Deserialize button event JSON
    serial_number = event["serialNumber"]
    click_type = event["clickType"]
    battery_voltage = event["batteryVoltage"]
    print(
        "Received button press from SN:{} with clickType {} and voltage {}".format(
            serial_number, click_type, battery_voltage
        )
    )

    # Get a reference to the database table
    dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
    table = dynamodb.Table(os.environ["CHORTLE_DYNAMO_TABLE"])

    # Query the chore entry corresponding to the button that was pressed
    event_key = {"button_serial": serial_number, "click_type": click_type}
    entry = table.get_item(Key=event_key)["Item"]
    print("Retrieved entry from table: {}".format(entry))

    for key, expr, expr_attrs in get_update_expression(entry):
        table.update_item(
            Key=key, UpdateExpression=expr, ExpressionAttributeValues=expr_attrs
        )
