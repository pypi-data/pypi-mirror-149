from pprint import pp

from cloudbuddy.constants import AWS_RDS_ENGINE, AWS_RDS_USERNAME, AWS_RDS_PASSWORD
from cloudbuddy.infra import get_vpc_configuration
from cloudbuddy.prettify_message import pprint
from time import sleep


def create_rds(client, region, vpc, db, time_zone, max_allocated_storage, delete_protection):
    subnet_group = str(db) + str(region)
    try:
        db_response = client.describe_db_instances(
            DBInstanceIdentifier=db
        )
        if db_response.get("DBInstances"):
            pprint.pretty_print(f"Database already exists - {db}", level="info")
    except Exception:
        pprint.pretty_print(
            "Databse not found, creation one!!!", level="debug")
        subnet, security_group, vpc_id = get_vpc_configuration(vpc, region)
        try:
            subnet_group_response = client.describe_db_subnet_groups(
                DBSubnetGroupName=subnet_group)
            if subnet_group_response.get("DBSubnetGroups"):
                pprint.pretty_print(
                    f"DB subnet group already exists - {subnet_group}", level='info')
        except Exception as e:
            pprint.pretty_print(
                "SB subnet group not found, creating one!!!", level='debug')
            client.create_db_subnet_group(
                DBSubnetGroupName=subnet_group,
                DBSubnetGroupDescription="This is sample rds subnet group",
                SubnetIds=subnet
            )
            pprint.pretty_print(f"DB subnet group created - {subnet_group}", level='debug')
        try:
            pprint.pretty_print(
                f"Creating database with DBName - {db}", level='debug')
            client.create_db_instance(
                DBName=db,
                AllocatedStorage=5,
                DBInstanceClass="db.t3.micro",
                # This can be unique for now I have kept it same as db_name to make it easy
                DBInstanceIdentifier=db,
                Engine=AWS_RDS_ENGINE,  # this we can read from sample yml
                MasterUserPassword=AWS_RDS_PASSWORD,
                MasterUsername=AWS_RDS_USERNAME,
                DBSubnetGroupName=subnet_group,
                VpcSecurityGroupIds=security_group,
                Timezone=time_zone,
                MaxAllocatedStorage=max_allocated_storage,
                DeletionProtection=delete_protection
            )
            pprint.pretty_print(
                f"Created database with DBName - {db}", level='debug')
        except Exception as ex:
            if ex.response["Error"]["Code"] == "DBInstanceAlreadyExistsFault":
                    pprint.pretty_print(
                        f"DB instance already exists for the database that you are trying to create. Please check {ex}",
                        level="error")
            elif ex.response["Error"]["Code"] == "DBParameterGroupNotFoundFault":
                pprint.pretty_print(f"DB parameter group not found Please check {ex}", level="error")
            elif ex.response["Error"]["Code"] == "DBSecurityGroupNotFoundFault":
                pprint.pretty_print(f"DB security group not found. Please check: {ex}", level="error")
            elif ex.response["Error"]["Code"] == "DBSubnetGroupNotFoundFault":
                pprint.pretty_print(f"DB subnet group not found. Please check: {ex}", level="error")
            elif ex.response["Error"]["Code"] == "DBSubnetGroupDoesNotCoverEnoughAZs":
                pprint.pretty_print(f"DB subnet group does not cover enough AZs. Please check: {ex}", level="error")
            elif ex.response["Error"]["Code"] == "InvalidDBClusterStateFault":
                pprint.pretty_print(f"Invalid DB Cluster state. Please check: {ex}", level="error")
            elif ex.response["Error"]["Code"] == "InvalidSubnet":
                pprint.pretty_print(f"Invalid subnet used to create db instance. Please check: {ex}", level="error")
            elif ex.response["Error"]["Code"] == "InvalidVPCNetworkStateFault":
                pprint.pretty_print(f"In valid VPC network used to create DB instance. Please check {ex}",
                                    level="error")
            elif ex.response["Error"]["Code"] == "DBClusterNotFoundFault":
                pprint.pretty_print(f"The specified DB Cluster Not found. Please check: {ex}", level="error")
            elif ex.response["Error"]["Code"] == "StorageTypeNotSupportedFault":
                pprint.pretty_print(f"The specified Storage Type is not supported. Please check: {ex}",
                                    level="error")
            elif ex.response["Error"]["Code"] == "AuthorizationNotFoundFault":
                pprint.pretty_print(
                    f"RDS might not be authorized to perform necessary actions using IAM on your behalf. Please check {ex}",
                    level="error")
            elif ex.response["Error"]["Code"] == "DomainNotFoundFault":
                pprint.pretty_print(
                    f"Domain doesn't refer to an existing Active Directory domain. Please check {ex}",
                    level="error")
            else:
                pprint.pretty_print(
                    f"Unexpected error occurred while creating RDS database Instance. Please check {ex}",
                    level="error")


def delete_rds(client, db):
    try:
        db_response = client.describe_db_instances(
            DBInstanceIdentifier=db
        )
        if db_response.get("DBInstances"):
            pprint.pretty_print("Database exists", level="info")
            pprint.pretty_print("Deleting database", level="debug")
            if db_response.get("DBInstances")[0].get("DBInstanceStatus") != "deleting":
                try:
                    client.delete_db_instance(
                        DBInstanceIdentifier=db,
                        SkipFinalSnapshot=True
                    )
                    pprint.pretty_print(f"Database deleted - {db}", level="debug")
                except Exception as e:
                    print(e)
                    pprint.pretty_print(
                        "Database deletion failed", level="error")
            else:
                pprint.pretty_print("Database already deleted", level="info")
    except Exception as e:
        pprint.pretty_print(f"{db} - Database does not exist", level='info')


def delete_subnet(client, region, db):
    subnet_group = str(db) + str(region)
    try:
        subnet_group_response = client.describe_db_subnet_groups(
            DBSubnetGroupName=subnet_group)
        if subnet_group_response.get("DBSubnetGroups"):
            pprint.pretty_print(
                "DB subnet group exists", level='info')
            pprint.pretty_print("Deleting subnet groups", level="debug")
            db_service = "deleting"
            if db_service == "deleting":
                while db_service == "deleting":
                    pprint.pretty_print(
                        "Databse getting deleted currently, please wait...", level="warning")
                    sleep(30)
                    try:
                        db_resp = client.describe_db_instances(
                            DBInstanceIdentifier=db)
                        db_service = db_resp.get("DBInstances")[
                            0].get("DBInstanceStatus")
                    except Exception as e:
                        try:
                            client.delete_db_subnet_group(
                                DBSubnetGroupName=subnet_group
                            )
                            pprint.pretty_print(
                                f"Subnet groups deleted - {subnet_group}", level="debug")
                            db_service = ""
                        except Exception as e:
                            pprint.pretty_print(
                                "Subnet group deletion failed", level="error")
    except Exception as e:
        pprint.pretty_print(f"{subnet_group} - Subnet group does not exist", level='info')


def rds_infra_creator(client, rds_resource_object):
    account_name = rds_resource_object.name
    account_prefix = rds_resource_object.prefix
    db_name = str(account_prefix) + str(account_name)
    vpc_name = str(account_prefix) + "-" + str(account_name)
    rds_region = rds_resource_object.region
    optional_params = rds_resource_object.rds_optional_params
    time_zone = optional_params.get("Timezone")
    max_allocated_storage = optional_params.get("MaxAllocatedStorage", 10)
    delete_protection = optional_params.get("DeletionProtection", False)
    create_rds(client, rds_region, vpc_name, db_name, time_zone, max_allocated_storage, delete_protection)


def rds_infra_deletion(client, rds_resource_object):
    account_name = rds_resource_object.name
    account_prefix = rds_resource_object.prefix
    db_name = str(account_prefix) + str(account_name)
    rds_region = rds_resource_object.region
    delete_rds(client, db_name)
    delete_subnet(client, rds_region, db_name)
