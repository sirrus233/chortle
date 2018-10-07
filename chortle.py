#!/usr/bin/python

import boto3
import time

if __name__ == '__main__':
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='chortle')

    while(True):
         messages = queue.receive_messages(MaxNumberOfMessages=1)
         num_messages_received = len(messages)
         print('Received {} messages from queue.'.format(num_messages_received))
         if num_messages_received > 0:
             message = messages[0]
             print(message.body)
             message.delete()
         time.sleep(6)
