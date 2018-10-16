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
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(CHORTLE_DYNAMO_TABLE)
    key = {'button_serial': serial_number, 'click_type': click_type}

    entry = table.get_item(Key=key)['Item']
    print('Retrieved entry from table: {}'.format(entry))

    try:
        expr, expr_attrs = get_update_expression(entry)
        table.update_item(Key=key, UpdateExpression=expr, ExpressionAttributeValues=expr_attrs)
    except UnknownStrategyException:
        print('Unknown strategy: {}'.format(entry['strategy']))
