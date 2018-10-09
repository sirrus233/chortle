import os
import boto3
import time


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
    
    current_time = int(time.time())
    key = {'button_serial': serial_number}
    expr = 'SET last_pressed_time=:t'
    expr_attrs = {':t': current_time}
    table.update_item(Key=key, UpdateExpression=expr, ExpressionAttributeValues=expr_attrs)
    print('Table updated with new timestamp {}'.format(current_time))
