from cloudbuddy.constants import VPC_CIDR_BLOCK_1, VPC_CIDR_BLOCK_2
from cloudbuddy.infra import create_boto_resource
from cloudbuddy.prettify_message import pprint


def is_vpc_exist(client, vpc_name):
    try:
        response_vpc = client.describe_vpcs(
            Filters=[
                {
                    "Name": "tag:Name",
                    "Values": [
                        vpc_name,
                    ]
                },
                {
                    "Name": "cidr-block-association.cidr-block",
                    "Values": [
                        VPC_CIDR_BLOCK_1,
                        VPC_CIDR_BLOCK_2
                    ]
                },
            ]
        )

    except Exception as ex:
        pprint.pretty_print(f"Unexpected Error. {ex}", level="error")
        return False

    if response_vpc.get("Vpcs"):
        return True
    return False


def create_vpc(client, name, region):
    # create VPC
    client_resource = create_boto_resource(region)
    vpc = client_resource.create_vpc(CidrBlock=VPC_CIDR_BLOCK_1)

    # assign a name to our VPC
    vpc.create_tags(Tags=[{"Key": "Name", "Value": name}])
    vpc.wait_until_available()

    # enable public dns hostname so that we can SSH into it later
    client.modify_vpc_attribute(VpcId=vpc.id, EnableDnsSupport={"Value": True})
    client.modify_vpc_attribute(
        VpcId=vpc.id, EnableDnsHostnames={"Value": True})
    pprint.pretty_print(f"VPC created - {name}", level="debug")
    pprint.pretty_print(
        f"CIDR block of the VPC - {VPC_CIDR_BLOCK_1}", level="debug")

    # associate alternate cidr_block to vpc
    client.associate_vpc_cidr_block(CidrBlock=VPC_CIDR_BLOCK_2,
                                    VpcId=vpc.id,)
    pprint.pretty_print(
        f"CIDR block of the VPC associated - {VPC_CIDR_BLOCK_2}", level="debug")

    # create an internet gateway and attach it to VPC
    internetgateway = client_resource.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)
    pprint.pretty_print(f"Gateway attached to vpc - {name}", level="debug")

    # Create a security group and allow SSH inbound rule through the VPC
    securitygroup = client_resource.create_security_group(
        GroupName="SSH-ONLY", Description="only allow SSH traffic", VpcId=vpc.id)
    securitygroup.authorize_ingress(
        CidrIp="0.0.0.0/0", IpProtocol="tcp", FromPort=22, ToPort=22)
    pprint.pretty_print(
        f"Security group created for VPC - {name}", level="debug")

    # create a route table and a public route- Optional as ig creation also creates a routetable and route
    response_route_table = client.describe_route_tables(
        Filters=[
            {
                "Name": "vpc-id",
                "Values": [
                    vpc.id
                ]
            }
        ]
    )
    if response_route_table["RouteTables"][0]["Associations"][0]["RouteTableId"]:
        route_table_id = response_route_table["RouteTables"][0]["Associations"][0]["RouteTableId"]
        client.create_route(
            DestinationCidrBlock="0.0.0.0/0", GatewayId=internetgateway.id, RouteTableId=route_table_id)
        pprint.pretty_print(
            "Route table created and public route established", level="debug")
        # create subnet and associate it with route table
        subnet_1 = client_resource.create_subnet(
            CidrBlock=VPC_CIDR_BLOCK_1, VpcId=vpc.id, AvailabilityZone='us-west-1a')
        subnet_2 = client_resource.create_subnet(
            CidrBlock=VPC_CIDR_BLOCK_2, VpcId=vpc.id, AvailabilityZone='us-west-1b')
        client.associate_route_table(
            SubnetId=subnet_1.id, RouteTableId=route_table_id)
        client.associate_route_table(
            SubnetId=subnet_2.id, RouteTableId=route_table_id)
        pprint.pretty_print(
            "Subnet created and associated with route table", level="debug")

    # TODO: Break into multiple small methods like create security group, create route table

    return True


def vpc_infra_creator(client, vpc_resource_object):
    account_name = vpc_resource_object.name
    account_prefix = vpc_resource_object.prefix
    vpc_name = str(account_prefix) + "-" + str(account_name)
    vpc_region = vpc_resource_object.region

    is_exist = is_vpc_exist(client, vpc_name)
    if is_exist:
        pprint.pretty_print(f"VPC already exist - {vpc_name}", level="info")
        return False

    vpc_response = create_vpc(client, vpc_name, vpc_region)
    if vpc_response is True:
        pprint.pretty_print(
            f"Successfully created the VPC - {vpc_name}", level="debug")
    else:
        pprint.pretty_print(
            f"Failed to create the VPC - {vpc_name}", level="error")