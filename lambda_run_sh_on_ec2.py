import json
import boto3
import paramiko

def get_key_from_s3(s3Bucket, s3Key, keyPath):
    s3_client = boto3.client('s3')
    s3_client.download_file(s3Bucket, s3Key, keyPath)


def run_sh_on_ec2(keyPath, host, username, commands):
    k = paramiko.RSAKey.from_private_key_file(keyPath)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    c.connect(hostname=host, username=username, pkey=k)

    for command in commands:
        print('exe : {}'.format(command))
        stdin, stdout, stderr = c.exec_command(command)
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))


def get_private_ip(instanceId):
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(Filters = [{
        'Name' : 'instance-id',
        'Values' : [instanceId]}])

    for instance in instances:
        print(instance.private_ip_address)
        return instance.private_ip_address


def lambda_handler(event, context):
    print('lambda_handler')
    print("Received event: " + json.dumps(event, indent=2))
    message = json.loads(event['Records'][0]['Sns']['Message'])

    private_ip = get_private_ip(message['EC2InstanceId'])

    s3Bucket = 'bucket_name'
    s3Key = 'key_name'
    keyPath = '/tmp/key'
    get_key_from_s3(s3Bucket, s3Key, keyPath)

    host = private_ip
    username = 'user_name'
    commands = [
        'ls -al'
    ]
    run_sh_on_ec2(keyPath, host, username, commands)

# test
if __name__ == '__main__':
    import sys

    instance_id = sys.argv[1]
    private_ip = get_private_ip(instance_id)

    s3Bucket = sys.argv[2]
    s3Key = sys.argv[3]
    keyPath = sys.argv[4]
    get_key_from_s3(s3Bucket, s3Key, keyPath)

    host = sys.argv[5]
    username = sys.argv[6]
    commands = [
        'ls -al'
    ]
    run_sh_on_ec2(keyPath, host, username, commands)


