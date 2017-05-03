import json
import boto3
import time

print('as-lifecycle-hook-handler')

client = boto3.client('autoscaling')


def do_something():
    print('do something..')
    time.sleep(2)
    print('done')


def lambda_handler(event, context):
    print('lambda-handler')
    print("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])
    # metadata = message['NotificationMetatdata']

    do_something()

    response = client.complete_lifecycle_action(
        LifecycleHookName=message['LifecycleHookName'],
        AutoScalingGroupName=message['AutoScalingGroupName'],
        LifecycleActionResult='CONTINUE',
        InstanceId=message['EC2InstanceId']
    )
    print(response)

