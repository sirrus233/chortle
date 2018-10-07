import json
import boto3
import os

CHORTLE_SNS_TOPIC = os.environ['CHORTLE_SNS_TOPIC'] 

def lambda_handler(event, context):
    # Deserialize button event JSON
    serial_number = event['serialNumber']
    click_type = event['clickType']
    battery_voltage = event['batteryVoltage']
    
    sns_client = boto3.client('sns')
    message = serial_number
    response = sns_client.publish(TopicArn=CHORTLE_SNS_TOPIC, Message=message)
    
    print('Sent message: {} with response {}'.format(message, response))
