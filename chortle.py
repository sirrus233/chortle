#!/usr/bin/python

import boto3
import json
import time
from datetime import datetime
from threading import Thread


class UpdateChoreStatus(Thread):
    def run(self):
        dynamo = boto3.resource('dynamodb')
        table = dynamo.Table('chortle-model')

        while(True):
            for item in table.scan()['Items']:
                current_time = datetime.now()
                last_pressed_time = datetime.fromisoformat(item['last_pressed_time'])
                time_diff_seconds = (current_time - last_pressed_time).seconds
                status_ok = time_diff_seconds < item['reset_time_seconds']
                if status_ok != item['status_ok']:
                    table.update_item(
                            Key={'button_serial': item['button_serial']},
                            UpdateExpression='SET status_ok=:s',
                            ExpressionAttributeValues={':s': status_ok})
            time.sleep(2)


class ProcessButtonPresses(Thread):
    def run(self):
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName='chortle')

        dynamo = boto3.resource('dynamodb')
        table = dynamo.Table('chortle-model')

        while(True):
            messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
            for message in messages:
                message_json = json.loads(message.body)
                button_serial = message_json['Message']

                table.update_item(
                        Key={'button_serial': button_serial},
                        UpdateExpression='SET last_pressed_time=:t',
                        ExpressionAttributeValues={':t': datetime.isoformat(datetime.now(), timespec='seconds')})

                message.delete()


if __name__ == '__main__':
    ProcessButtonPresses().start()
    UpdateChoreStatus().start()
