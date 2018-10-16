import os
import boto3

from strategy_handler import get_update_expression, UnknownStrategyException


CHORTLE_DYNAMO_TABLE = os.environ['CHORTLE_DYNAMO_TABLE']


def lambda_handler(event, context):
    # Deserialize button event JSON
    serial_number = event['serialNumber']
    click_type = event['clickType']
    battery_voltage = event['batteryVoltage']
    print('Received button press from SN:{} with clickType {} and voltage {}'.format(
        serial_number, click_type, battery_voltage))

    # Get a reference to the database table
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(CHORTLE_DYNAMO_TABLE)

    # Query the chore entry corresponding to the button that was pressed
    event_key = {'button_serial': serial_number, 'click_type': click_type}
    entry = table.get_item(Key=event_key)['Item']
    print('Retrieved entry from table: {}'.format(entry))

    try:
        for key, expr, expr_attrs in get_update_expression(entry):
            table.update_item(Key=key, UpdateExpression=expr, ExpressionAttributeValues=expr_attrs)
    except UnknownStrategyException:
        print('Unknown strategy: {}'.format(entry['strategy']))
