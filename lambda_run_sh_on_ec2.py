import json
import boto3
import paramiko

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


# test
if __name__ == '__main__':
    import sys

    instance_id = sys.argv[1]
    private_ip = get_private_ip(instance_id)

    key = sys.argv[2]
    host = sys.argv[3]
    username = sys.argv[4]
    commands = [
        'ls -al'
    ]

    run_sh_on_ec2(key, host, username, commands)


