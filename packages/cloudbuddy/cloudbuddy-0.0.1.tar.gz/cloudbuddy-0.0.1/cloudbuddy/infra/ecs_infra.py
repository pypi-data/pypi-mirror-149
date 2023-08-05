from cloudbuddy.constants import AWS_CLUSTER_NAME, AWS_TASK_NAME, REPOSITORY_NAME, IMAGE_TAG, AWS_CPU, AWS_MEMORY
from cloudbuddy.constants import AWS_SERVICE_NAME, DESIRED_COUNT
from cloudbuddy.infra import get_vpc_configuration
from cloudbuddy.config import AWS_ACCOUNT_ID
from botocore.exceptions import ClientError
from time import sleep
from cloudbuddy.prettify_message import pprint


def create_cluster(client):
    pprint.pretty_print(f"Creating cluster {AWS_CLUSTER_NAME}", level="debug")
    try:
        client.create_cluster(clusterName=AWS_CLUSTER_NAME)
        pprint.pretty_print(f"Successfully created Cluster - {AWS_CLUSTER_NAME}", level="debug")
    except ClientError as e:
        pprint.pretty_print("Cluster creation failed", level="error")
        if e.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(e, level="error")
        exit()


def create_task(client, region):
    try:
        response = client.describe_task_definition(
            taskDefinition=AWS_TASK_NAME)
        if response.get("taskDefinition"):
            pprint.pretty_print(f"Task already exists - {AWS_TASK_NAME}", level="info")
        else:
            pprint.pretty_print(
                "Failed to create task definiton", level="warning")
    except Exception as e:
        pprint.pretty_print("Creating task", level="debug")
        try:
            response = client.register_task_definition(
                containerDefinitions=[
                    {
                        "name": REPOSITORY_NAME,
                        "image": f"{REPOSITORY_NAME}/{IMAGE_TAG}",
                        "cpu": 256,
                        "portMappings": [],
                        "essential": True,
                        "environment": [],
                        "mountPoints": [],
                        "volumesFrom": [],
                        "logConfiguration": {
                            "logDriver": "awslogs",
                            "options": {
                                "awslogs-group": "/ecs/AWSSampleApp",
                                "awslogs-region": region,
                                "awslogs-stream-prefix": "ecs"
                            }
                        }
                    }
                ],
                executionRoleArn="arn:aws:iam::" +
                f"{AWS_ACCOUNT_ID}"+":role/ecsTaskExecutionRole",
                family=AWS_TASK_NAME,
                networkMode="awsvpc",
                requiresCompatibilities=[
                    "FARGATE"
                ],
                cpu=AWS_CPU,
                memory=AWS_MEMORY)
            pprint.pretty_print(f"Task definition created - {AWS_TASK_NAME}", level="debug")
        except ClientError as e:
            pprint.pretty_print(
                "Failed to create task definiton", level="error")
            if e.response["Error"]["Code"] == "InvalidParameterException":
                pprint.pretty_print(e, level="error")


def create_service(client, name, region, service_configuration):
    pprint.pretty_print("Creating Service", level="debug")
    subnets, security_groups, vpc_id = get_vpc_configuration(name, region)
    try:
        check_service = client.describe_services(cluster=AWS_CLUSTER_NAME,
                                                 services=[AWS_SERVICE_NAME])
        if len(check_service.get("services")) > 0:
            if check_service["services"][0]["status"] == "ACTIVE":
                pprint.pretty_print(
                    f"Service already exists and active - {AWS_SERVICE_NAME}", level="info")
            elif check_service["services"][0]["status"] == "INACTIVE":
                client.create_service(cluster=AWS_CLUSTER_NAME,
                                      serviceName=AWS_SERVICE_NAME,
                                      taskDefinition=AWS_TASK_NAME,
                                      desiredCount=DESIRED_COUNT,
                                      networkConfiguration={
                                          "awsvpcConfiguration": {
                                              "subnets": subnets,
                                              "assignPublicIp": "ENABLED",
                                              "securityGroups": security_groups
                                          }
                                      },
                                      launchType="FARGATE",
                                      deploymentConfiguration=service_configuration
                                      )
                pprint.pretty_print(f"Service created - {AWS_SERVICE_NAME}", level="debug")
            elif check_service["services"][0]["status"] == "DRAINING":
                while check_service["services"][0]["status"] == "DRAINING":
                    pprint.pretty_print(
                        "Previous service is getting completed. Please wait!!!", level="info")
                    sleep(10)
                    check_service = client.describe_services(cluster=AWS_CLUSTER_NAME,
                                                             services=[AWS_SERVICE_NAME])
                client.create_service(cluster=AWS_CLUSTER_NAME,
                                      serviceName=AWS_SERVICE_NAME,
                                      taskDefinition=AWS_TASK_NAME,
                                      desiredCount=DESIRED_COUNT,
                                      networkConfiguration={
                                          "awsvpcConfiguration": {
                                              "subnets": subnets,
                                              "assignPublicIp": "ENABLED",
                                              "securityGroups": security_groups
                                          }
                                      },
                                      launchType="FARGATE",
                                      deploymentConfiguration=service_configuration
                                      )
                pprint.pretty_print(f"Service created - {AWS_SERVICE_NAME}", level="debug")
        else:
            client.create_service(cluster=AWS_CLUSTER_NAME,
                                  serviceName=AWS_SERVICE_NAME,
                                  taskDefinition=AWS_TASK_NAME,
                                  desiredCount=DESIRED_COUNT,
                                  networkConfiguration={
                                      "awsvpcConfiguration": {
                                          "subnets": subnets,
                                          "assignPublicIp": "ENABLED",
                                          "securityGroups": security_groups
                                      }
                                  },
                                  launchType="FARGATE",
                                  deploymentConfiguration=service_configuration
                                  )
            pprint.pretty_print(f"Service created - {AWS_SERVICE_NAME}", level="debug")
    except Exception as e:
        print(e)
        # if e.response["Error"]["Code"] == "InvalidParameterException":
        #     pprint.pretty_print(e, level="error")
        # elif e.response["Error"]["Code"] == "ClusterNotFoundException":
        #     raise e
        # elif e.response["Error"]["Code"] == "PlatformTaskDefinitionIncompatibilityException":
        #     raise e
        # elif e.response["Error"]["Code"] == "AccessDeniedException":
        #     raise e
        # elif e.response["Error"]["Code"] == "PlatformUnknownException":
        #     raise e
        # elif e.response["Error"]["Code"] == "PlatformTaskDefinitionIncompatibilityException":
        #     raise e
        # elif e.response["Error"]["Code"] == "ClientException":
        #     raise e
        pprint.pretty_print("Service creation failed, please retry...", level="error")


def delete_cluster(client):
    pprint.pretty_print(f"Deleting cluster {AWS_CLUSTER_NAME}", level="debug")
    try:
        client.delete_cluster(cluster=AWS_CLUSTER_NAME)
        pprint.pretty_print(f"Successfully deleted Cluster - {AWS_CLUSTER_NAME}", level="debug")
    except ClientError as e:
        pprint.pretty_print("Cluster deletion failed", level="error")
        if e.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(e, level="error")


def delete_task(client):
    try:
        response = client.describe_task_definition(
            taskDefinition=AWS_TASK_NAME)
        if response.get("taskDefinition"):
            task_arn = response.get("taskDefinition").get("taskDefinitionArn")
            pprint.pretty_print(f"Task definiton exists - {AWS_TASK_NAME}", level="info")
            pprint.pretty_print("Deleting task definition", level="debug")
            client.deregister_task_definition(
                taskDefinition=task_arn
            )
            pprint.pretty_print(f"Task definition deleted - {AWS_TASK_NAME}", level="debug")
    except ClientError as e:
        pprint.pretty_print(
            f"{AWS_TASK_NAME} - Task definition does not exist", level="info")
        if e.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(e, level="error")


def delete_service(client):
    try:
        check_service = client.describe_services(cluster=AWS_CLUSTER_NAME,
                                                 services=[AWS_SERVICE_NAME])
        if len(check_service.get("services")) > 0:
            if check_service["services"][0]["status"] == "ACTIVE":
                pprint.pretty_print(
                    f"{AWS_SERVICE_NAME} - Service exists and active", level="info")
                pprint.pretty_print("Deleting service", level="debug")
                try:
                    client.update_service(cluster=AWS_CLUSTER_NAME,
                                        service=AWS_SERVICE_NAME,
                                        desiredCount=0)
                    client.delete_service(
                        cluster=AWS_CLUSTER_NAME,
                        service=AWS_SERVICE_NAME,
                        force=False
                    )
                except Exception as e:
                    print(e)
                pprint.pretty_print("Service deleted", level="debug")
            elif check_service["services"][0]["status"] == "INACTIVE":
                pprint.pretty_print("Service already deleted", level="info")
            elif check_service["services"][0]["status"] == "DRAINING":
                while check_service["services"][0]["status"] == "DRAINING":
                    pprint.pretty_print(
                        "Service is currently getting deleted. Please wait!!!", level="info")
                    sleep(10)
                    check_service = client.describe_services(cluster=AWS_CLUSTER_NAME,
                                                             services=[AWS_SERVICE_NAME])
                pprint.pretty_print(f"Service deleted- {AWS_SERVICE_NAME}", level="debug")
        else:
            pprint.pretty_print(f"{AWS_SERVICE_NAME} - Service does not exist", level="info")
    except ClientError as e:
        if e.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(e, level="error")
        elif e.response["Error"]["Code"] == "ClusterNotFoundException":
            raise e
        elif e.response["Error"]["Code"] == "PlatformTaskDefinitionIncompatibilityException":
            raise e
        elif e.response["Error"]["Code"] == "AccessDeniedException":
            raise e
        elif e.response["Error"]["Code"] == "PlatformUnknownException":
            raise e
        elif e.response["Error"]["Code"] == "PlatformTaskDefinitionIncompatibilityException":
            raise e
        elif e.response["Error"]["Code"] == "ClientException":
            raise e
        pprint.pretty_print("Service deletion failed", level="error")
        exit()


def ecs_infra_creator(client, ecs_resource_object):
    account_name = ecs_resource_object.name
    account_prefix = ecs_resource_object.prefix
    vpc_name = str(account_prefix) + "-" + str(account_name)
    ecs_region = ecs_resource_object.region
    optional_params = ecs_resource_object.ecs_optional_params
    service_configuration = optional_params.get("deploymentConfiguration", {
        'deploymentCircuitBreaker': {
            'enable': False,
            'rollback': False
        },
        'maximumPercent': 200,
        'minimumHealthyPercent': 0
    })
    #health_check_grace_period_seconds = optional_params.get("healthCheckGracePeriodSeconds", 30) To be included later once load balancer code included
    create_cluster(client)
    create_task(client, ecs_region)
    create_service(client, vpc_name, ecs_region, service_configuration)


def ecs_infra_deletion(client, ecs_resource_object):
    delete_service(client)
    delete_task(client)
    delete_cluster(client)
