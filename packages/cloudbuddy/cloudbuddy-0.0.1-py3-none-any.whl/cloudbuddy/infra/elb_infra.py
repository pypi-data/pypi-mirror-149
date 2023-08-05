from pprint import pp
from botocore.exceptions import ClientError
from cloudbuddy.prettify_message import pprint
from cloudbuddy.infra import get_vpc_configuration
import random


# Get arn for load balancer and target groups
def get_arn(client, lb_name, tg_name_1, tg_name_2):
    response_elb = client.describe_load_balancers(Names=[lb_name])
    resp_elb = response_elb["LoadBalancers"][0]["LoadBalancerArn"]
    response_tg = client.describe_target_groups(Names=[tg_name_1, tg_name_2])
    resp_tg = [i["TargetGroupArn"] for i in response_tg["TargetGroups"]]
    return resp_tg, resp_elb


# Get arn for load balancer and target groups and listener in list format
def get_arn_list(client, lb_name, tg_name_1, tg_name_2):
    try:
        tg_arn, lb_arn = get_arn(client, lb_name, tg_name_1, tg_name_2)
        response_listener = client.describe_listeners(LoadBalancerArn=lb_arn)
        resp_listener = response_listener["Listeners"]
    except Exception as e:
        pprint.pretty_print("Listeners do not exist", level="info")
    try:
        response_tg = client.describe_target_groups(
            Names=[tg_name_1, tg_name_2])
        resp_tg = response_tg["TargetGroups"]
    except Exception:
        pprint.pretty_print(
            f"Target groups do not exist - {tg_name_1} | {tg_name_2}", level="info")
    try:
        response_elb = client.describe_load_balancers(Names=[lb_name])
        resp_elb = response_elb["LoadBalancers"]
    except Exception:
        pprint.pretty_print(
            f"Load Balancer does not exist - {lb_name}", level="info")
    return resp_listener, resp_tg, resp_elb

# Create ALB
def create_alb(client, name, subnet, sec_group):
    try:
        client.describe_load_balancers(Names=[name])
        pprint.pretty_print(
            f"Load balancer already exists - {name}", level="info")
    except ClientError as e:
        pprint.pretty_print(
            "Load balancer does not exist. Creating one!!!", level="debug")
        try:
            client.create_load_balancer(Name=name,
                                        Subnets=subnet,
                                        SecurityGroups=sec_group,
                                        Scheme='internet-facing',
                                        IpAddressType='ipv4',
                                        Type='application')
        except ClientError as e:
            pprint.pretty_print(e, level="error")
            pprint.pretty_print("Load balancer creation failed", level="error")
            exit()
        pprint.pretty_print(f"Load balancer created - {name}", level="debug")


# Create Target Group
def create_tg(client, name_1, name_2, vpc_id):
    try:
        client.describe_target_groups(Names=[name_1, name_2])
        pprint.pretty_print(
            f"Target Groups already exists - {name_1} | {name_2}", level="info")
    except ClientError as e:
        pprint.pretty_print(
            'Target Groups do not exist. Creating!!!', level="debug")
        try:
            client.create_target_group(
                Name=name_1, Protocol='HTTP', Port=80, VpcId=vpc_id, TargetType="ip", HealthCheckProtocol='HTTP',
                HealthCheckPort="81", HealthCheckEnabled=True, HealthCheckPath='/health')
            client.create_target_group(
                Name=name_2, Protocol='HTTP',  Port=80, VpcId=vpc_id, TargetType="ip", HealthCheckProtocol='HTTP',
                HealthCheckPort="81", HealthCheckEnabled=True, HealthCheckPath='/health')
        except ClientError as e:
            pprint.pretty_print(e, level="error")
            pprint.pretty_print("Target group creation failed", level="error")
            exit()
        pprint.pretty_print(
            f"Target Groups created - {name_1} | {name_2}", level="debug")

# Create Listener
def create_listener(client, alb, tg):
    try:
        response_listener = client.describe_listeners(
            LoadBalancerArn=alb)
        resp = response_listener["Listeners"]
        if resp:
            pprint.pretty_print("Listeners already exists", level="info")
        else:
            pprint.pretty_print(
                "Listeners do not exist. Creating!!!", level="debug")
            client.create_listener(DefaultActions=[
                {
                    "Type": "forward",
                    "ForwardConfig": {
                        "TargetGroups": [
                            {
                                "TargetGroupArn": tg_arn,
                                "Weight": random.randint(10, 50)
                            } for tg_arn in tg
                        ]
                    }
                }
            ],
                LoadBalancerArn=alb,
                Port=80,
                Protocol='HTTP',
            )
            pprint.pretty_print("Listeners created", level="debug")
    except ClientError as e:
        pprint.pretty_print(e, level="error")
        pprint.pretty_print("Listener creation failed", level="error")

# Create ALB
def delete_alb(client, alb, name):
    try:
        pprint.pretty_print(f"Deleting load balancers - {name}", level="debug")
        for rec in alb:
            alb_arn = rec.get("LoadBalancerArn")
            client.delete_load_balancer(
                LoadBalancerArn=alb_arn
            )
        pprint.pretty_print(f"Load balancer deleted - {name}", level="debug")
    except Exception as e:
        pprint.pretty_print(
            f"Load balancer deletion failed - {name}", level="error")


# Create Target Group
def delete_tg(client, tg, name_1, name_2):
    try:
        pprint.pretty_print(
            f"Deleting target groups - {name_1} | {name_2}", level="debug")
        for rec in tg:
            tg_arn = rec.get("TargetGroupArn")
            client.delete_target_group(
                TargetGroupArn=tg_arn
            )
        pprint.pretty_print(
            f"Target groups deleted - {name_1} | {name_2}", level="debug")
    except Exception as e:
        pprint.pretty_print(
            f"{name_1} | {name_2}Target group deletion failed", level="error")

# Create Listener


def delete_listener(client, listener):
    try:
        pprint.pretty_print("Deleting listeners", level="debug")
        for rec in listener:
            listener_arn = rec.get("ListenerArn")
            client.delete_listener(
                ListenerArn=listener_arn
            )
        pprint.pretty_print("Listensers deleted", level="debug")
    except ClientError as e:
        pprint.pretty_print("Listener deletion failed", level="error")


def elb_infra_creator(client, elb_resource_object):
    account_name = elb_resource_object.name
    account_prefix = elb_resource_object.prefix
    vpc_name = str(account_prefix) + "-" + str(account_name)
    region = elb_resource_object.region
    alb_name = elb_resource_object.alb
    tg_1 = alb_name + "-" + "tg-1"
    tg_2 = alb_name + "-" + "tg-2"
    subnets, security_groups, vpc_id = get_vpc_configuration(vpc_name, region)
    create_alb(client, alb_name, subnets, security_groups)
    create_tg(client, tg_1, tg_2, vpc_id)
    tg_arn, alb_arn = get_arn(client, alb_name, tg_1, tg_2)
    create_listener(client, alb_arn, tg_arn)


def elb_infra_deletion(client, elb_resource_object):
    alb_name = elb_resource_object.alb
    tg_1 = alb_name + "-" + "tg-1"
    tg_2 = alb_name + "-" + "tg-2"
    listener_arn, tg_arn, alb_arn = get_arn_list(client, alb_name, tg_1, tg_2)
    delete_listener(client, listener_arn)
    delete_tg(client, tg_arn, tg_1, tg_2)
    delete_alb(client, alb_arn, alb_name)
