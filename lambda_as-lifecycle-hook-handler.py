import json
import boto3
import time

def do_something():
    print('do something..')
    time.sleep(2)
    print('done')

def as_complete_lifecycle_action(lifecycleHookName, autoScalingGroupName, instanceId):
    print('as_complete_lifecycle_action : {}, {}, {}'.format(lifecycleHookName, autoScalingGroupName, instanceId))
    as_client = boto3.client('autoscaling')
    return as_client.complete_lifecycle_action(
        LifecycleHookName=lifecycleHookName,
        AutoScalingGroupName=autoScalingGroupName,
        InstanceId=instanceId,
        LifecycleActionResult='CONTINUE'
    )


def lambda_handler(event, context):
    print('lambda_handler')
    print("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])

    do_something()

    response = as_complete_lifecycle_action(message['LifecycleHookName'],
                                            message['AutoScalingGroupName'],
                                            message['EC2InstanceId'])

    print(response)
