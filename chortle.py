#!/usr/bin/python

import boto3
import json
from datetime import datetime


if __name__ == '__main__':
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='chortle')

    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('chortle-model')

    while(True):
         messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
         for message in messages:
             message_json = json.loads(message.body)
             button_serial = message_json['Message']

             #table.get_item(Key={'button_serial': button_serial})
             table.update_item(
                     Key={'button_serial': button_serial},
                     UpdateExpression='SET last_pressed_time=:t',
                     ExpressionAttributeValues={':t': datetime.isoformat(datetime.now(), timespec='seconds')})

             message.delete()
