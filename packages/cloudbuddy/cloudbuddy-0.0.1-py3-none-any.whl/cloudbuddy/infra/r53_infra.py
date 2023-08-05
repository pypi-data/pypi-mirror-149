from cloudbuddy.infra import get_vpc_configuration
from botocore.exceptions import ClientError
from cloudbuddy.prettify_message import pprint
import datetime
import random


# Create private hosted DNS zone
def create_zone(client, vpc_id, region, name):
    try:
        response_r53 = client.list_hosted_zones_by_vpc(VPCId=vpc_id,
                                                       VPCRegion=region
                                                       )
        if len(response_r53.get("HostedZoneSummaries")) > 0:
            pprint.pretty_print(f"Private DNS Zone exists - {name}", level="info")
        else:
            pprint.pretty_print(
                'Private DNS Zone does not exist. Creating One!!!', level="debug")
            client.create_hosted_zone(Name=name,
                                      VPC={
                                          'VPCRegion': region,
                                          'VPCId': vpc_id
                                      },
                                      CallerReference=str(datetime.datetime.now()))
            pprint.pretty_print(f"Private DNS Zone created - {name}", level="debug")
    except ClientError as e:
        pprint.pretty_print(e)
        pprint.pretty_print('Private DNS Zone creation failed', level="error")
        exit()

# Create DNS Zone resource record


def create_resource_record(client, vpc_id, region, name):
    try:
        response_r53 = client.list_hosted_zones_by_vpc(VPCId=vpc_id,
                                                       VPCRegion=region
                                                       )
        if len(response_r53.get("HostedZoneSummaries")) > 0:
            hostedzone = response_r53.get("HostedZoneSummaries")[
                0].get("HostedZoneId")
        pprint.pretty_print("Creating DNS Zone resource record", level="debug")
        client.change_resource_record_sets(ChangeBatch={
            'Changes': [
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'ResourceRecords': [
                            {
                                'Value': '10.0.0.0',
                            },
                        ],
                        'SetIdentifier': 'Test-1',
                        'TTL': 60,
                        'Type': 'A',
                        'Weight': random.randint(10, 50)
                    },
                },
                {
                    'Action': 'UPSERT',
                    'ResourceRecordSet': {
                        'Name': name,
                        'ResourceRecords': [
                            {
                                'Value': '10.0.0.1',
                            },
                        ],
                        'SetIdentifier': 'Test-2',
                        'TTL': 60,
                        'Type': 'A',
                        'Weight': random.randint(10, 50)
                    },
                },
            ],
        },
            HostedZoneId=hostedzone)
        pprint.pretty_print("DNS Zone resource record created", level="debug")
    except ClientError as e:
        pprint.pretty_print(e)
        pprint.pretty_print(
            "DNS Zone resource record creation failed", level="error")
        exit()

# Create private hosted DNS zone


def delete_zone(client, vpc_id, region, name):
    try:
        response_r53 = client.list_hosted_zones_by_vpc(VPCId=vpc_id,
                                                       VPCRegion=region
                                                       )
        if len(response_r53.get("HostedZoneSummaries")) > 0:
            pprint.pretty_print('Private DNS Zone exists', level="info")
            hostedzone = response_r53.get("HostedZoneSummaries")[
                0].get("HostedZoneId")
            pprint.pretty_print(f"Deleting private DNS zone - {name}", level="debug")
            try:
                client.delete_hosted_zone(
                    Id=hostedzone
                )
                pprint.pretty_print(
                    f"Private DNS hosted zone deleted - {name}", level="debug")
            except Exception as e:
                print(e)
                pprint.pretty_print(
                    'Private DNS Zone creation failed', level="info")
        else:
            pprint.pretty_print(
                f"{name} - Private DNS Zone does not exist", level="info")
    except Exception as e:
        pprint.pretty_print(e)

# Create DNS Zone resource record


def delete_resource_record(client, vpc_id, region, name):
    try:
        response_r53 = client.list_hosted_zones_by_vpc(VPCId=vpc_id,
                                                       VPCRegion=region
                                                       )
        if len(response_r53.get("HostedZoneSummaries")) > 0:
            hostedzone = response_r53.get("HostedZoneSummaries")[
                0].get("HostedZoneId")
            response_rr = client.list_resource_record_sets(
                HostedZoneId=hostedzone,
                StartRecordName=name,
                StartRecordType='A'
            )
            list_rr = response_rr.get("ResourceRecordSets")
            if list_rr:
                pprint.pretty_print(
                    "Deleting DNS Zone resource record", level="debug")
                try:
                    for rec in list_rr:
                        if rec.get("Type") == "A":
                            client.change_resource_record_sets(HostedZoneId=hostedzone,
                                                               ChangeBatch={
                                                                   'Changes': [
                                                                       {
                                                                           'Action': 'DELETE',
                                                                           'ResourceRecordSet': rec
                                                                       }
                                                                   ]
                                                               }
                                                               )
                    pprint.pretty_print(
                        "DNS Zone resource record deleted", level="debug")
                except Exception as e:
                    print(e)
                    pprint.pretty_print(
                        "DNS Zone resource record deletion failed", level="error")
        else:
            pprint.pretty_print(
                "DNS Zone resource record does not exist", level="info")
    except Exception as e:
        pprint.pretty_print(e)


def r53_infra_creator(client, r53_resource_object):
    account_name = r53_resource_object.name
    account_prefix = r53_resource_object.prefix
    vpc_name = str(account_prefix) + "-" + str(account_name)
    region = r53_resource_object.region
    subdomain = r53_resource_object.subdomain
    domain = r53_resource_object.domain
    subnets, security_groups, vpc = get_vpc_configuration(vpc_name, region)
    zone_name = subdomain+"."+domain
    create_zone(client, vpc, region, zone_name)
    create_resource_record(client, vpc, region, zone_name)


def r53_infra_deletion(client, r53_resource_object):
    account_name = r53_resource_object.name
    account_prefix = r53_resource_object.prefix
    vpc_name = str(account_prefix) + "-" + str(account_name)
    region = r53_resource_object.region
    subdomain = r53_resource_object.subdomain
    domain = r53_resource_object.domain
    subnets, security_groups, vpc = get_vpc_configuration(vpc_name, region)
    zone_name = subdomain+"."+domain
    delete_resource_record(client, vpc, region, zone_name)
    delete_zone(client, vpc, region, zone_name)
