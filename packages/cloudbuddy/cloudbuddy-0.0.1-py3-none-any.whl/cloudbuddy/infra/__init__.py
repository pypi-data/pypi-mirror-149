import boto3

from cloudbuddy.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN
from cloudbuddy.constants import BOTO_CLIENT_NAMES, AWS_RESOURCE_TYPE_EC2, AWS_RESOURCE_TYPE_VPC


def create_boto_clients(region):
    clients = {}
    for boto_client_name in BOTO_CLIENT_NAMES:
        kwargs = {
            "aws_access_key_id": AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
            "region_name": region
        }

        if AWS_SESSION_TOKEN:
            kwargs["aws_session_token"] = AWS_SESSION_TOKEN

        client = boto3.client(
            boto_client_name, **kwargs
        )

        clients[boto_client_name] = client

    return clients

def create_boto_resource(region):
    boto_client_name = AWS_RESOURCE_TYPE_EC2
    kwargs = {
        "aws_access_key_id": AWS_ACCESS_KEY_ID,
        "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
        "region_name": region
    }

    if AWS_SESSION_TOKEN:
        kwargs["aws_session_token"] = AWS_SESSION_TOKEN

    client = boto3.resource(
        boto_client_name, **kwargs
    )

    return client

def get_vpc_configuration(vpc_name, region):
    boto_clients = create_boto_clients(region)
    client = boto_clients.get(AWS_RESOURCE_TYPE_VPC)
    vpc_configs = client.describe_vpcs(
        Filters=[{'Name': 'tag:Name', 'Values': [vpc_name]}])
    vpc_id = vpc_configs.get('Vpcs')[0].get('VpcId')
    subnets_config = client.describe_subnets(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    subnets = [config['SubnetId'] for config in subnets_config.get('Subnets')]
    securitygroup_config = client.describe_security_groups(
        Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    security_groups = [config['GroupId']
                       for config in securitygroup_config.get('SecurityGroups')]
    return subnets, security_groups, vpc_id
