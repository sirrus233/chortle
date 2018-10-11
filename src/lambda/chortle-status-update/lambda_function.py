import os
import boto3
import time


CHORTLE_DYNAMO_TABLE = os.environ['CHORTLE_DYNAMO_TABLE']
UPDATE_PERIOD_SECONDS = os.environ['UPDATE_PERIOD_SECONDS']


def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(CHORTLE_DYNAMO_TABLE)

    timeout = time.time() + 60
    while time.time() < timeout:
        print('Updating table status')
        table_items = table.scan()['Items'] 
        print('Received {} item(s) from table'.format(len(table_items)))

        for item in table_items:
            current_time = int(time.time())
            last_pressed_time = item['last_pressed_time']
            time_diff_seconds = current_time - last_pressed_time
            status_ok = time_diff_seconds < item['reset_time_seconds']

            if status_ok != item['status_ok']:
                print('Updating SN:{} Chore: {} with status {}'.format(item['button_serial'], item['chore'], status_ok))
                key = {'button_serial': item['button_serial']}
                expr = 'SET status_ok=:s'
                expr_attrs = {':s': status_ok}
                table.update_item(Key=key, UpdateExpression=expr, ExpressionAttributeValues=expr_attrs)
                print('Update complete')

        time.sleep(UPDATE_PERIOD_SECONDS)
