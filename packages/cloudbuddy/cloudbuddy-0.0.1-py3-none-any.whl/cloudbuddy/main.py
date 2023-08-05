import argparse
import logging
import os
import yaml
from cloudbuddy.aws_env import AWSEnv
from cloudbuddy.aws_resources.elb_resource import ELBResource
from cloudbuddy.aws_resources.vpc_resource import VPCAccount
from cloudbuddy.aws_resources.ecs_resource import ECSResource
from cloudbuddy.aws_resources.rds_resource import RDSResource
from cloudbuddy.aws_resources.r53_resource import R53Resource
from cloudbuddy.constants import ALL_SERVICES, ALLOWED_CONFIG_FILES, ALLOWED_AWS_RESOURCES, ALL_RESOURCE_DELETE
from cloudbuddy.constants import AWS_RESOURCE_VPC, AWS_RESOURCE_ECS, AWS_RESOURCE_RDS, AWS_RESOURCE_ELB, AWS_RESOURCE_R53
from cloudbuddy.infra import create_boto_clients
from cloudbuddy.infra.ecr_infra import check_ecr_repo_and_image
from cloudbuddy.infra.vpc_infra import vpc_infra_creator
from cloudbuddy.infra.ecs_infra import ecs_infra_creator, ecs_infra_deletion
from cloudbuddy.infra.rds_infra import rds_infra_creator, rds_infra_deletion
from cloudbuddy.infra.elb_infra import elb_infra_creator, elb_infra_deletion
from cloudbuddy.infra.r53_infra import r53_infra_creator, r53_infra_deletion

create_infra_mapping = {
    AWS_RESOURCE_VPC: vpc_infra_creator,
    AWS_RESOURCE_ELB: elb_infra_creator,
    AWS_RESOURCE_R53: r53_infra_creator,
    AWS_RESOURCE_RDS: rds_infra_creator,
    AWS_RESOURCE_ECS: ecs_infra_creator,
}

delete_infra_mapping = {
    AWS_RESOURCE_ECS: ecs_infra_deletion,
    AWS_RESOURCE_RDS: rds_infra_deletion,
    AWS_RESOURCE_R53: r53_infra_deletion,
    AWS_RESOURCE_ELB: elb_infra_deletion,
}


def get_infra_creator(resource_name):
    if create_infra_mapping.get(resource_name):
        return create_infra_mapping.get(resource_name)
    else:
        raise Exception(
            f"{resource_name} is not a valid or supported AWS resource.")


def get_infra_deletion(resource_name):
    if delete_infra_mapping.get(resource_name):
        return delete_infra_mapping.get(resource_name)
    else:
        raise Exception(
            f"{resource_name} is not a valid or supported AWS resource.")


def validate_config_data(profiles, targets, apps, env, boto_clients, delete, resource):
    if env not in targets:
        raise Exception("Invalid target or env name. Please provide the correct env name or 'all'. "
                        f"Allowed env names are {', '.join(map(str, targets))}.")

    given_targets = ALL_SERVICES if env is None else [env]
    is_valid = False

    for app in apps:
        profile = app.get("profile")
        if profile not in profiles:
            raise Exception(f"Invalid profile name provided for app {app}. "
                            f"Allowed profile names are {', '.join(profiles)}")

        if delete is None:
            if resource is ALL_SERVICES:
                for target in given_targets:
                    is_valid = check_ecr_repo_and_image(
                        boto_clients["ecr"], app["name"], targets[target]["imageTag"])
            else:
                is_valid = True
        else:
            is_valid = True

    return given_targets if is_valid else []


def parse_input_config_file(config_file, env, delete, resource):
    with open(config_file, 'r') as config_file:
        config = yaml.safe_load(config_file)

    if not config:
        raise Exception("Empty config file. No content in the config file.")

    account = config.get("account")
    profiles = config.get("profiles")
    targets = config.get("targets")
    apps = config.get("apps")

    boto_clients = create_boto_clients(account["region"])
    given_targets = validate_config_data(
        profiles, targets, apps, env, boto_clients, delete, resource)

    environments = []

    for target in given_targets:
        resources = []
        vpc_resource = VPCAccount(account)
        ecs_resource = ECSResource(account)
        rds_resource = RDSResource(account)
        elb_resource = ELBResource(account)
        r53_resource = R53Resource(account)

        resources.extend([vpc_resource, ecs_resource,
                         rds_resource, elb_resource,
                         r53_resource])

        environment = AWSEnv(target, resources)
        environments.append(environment)

    return environments, boto_clients


def create_infra(env, boto_clients, resource):
    for res in env.resources:
        if resource == res.resource_name:
            try:
                client = boto_clients.get(res.resource_type)
                infra_creator = get_infra_creator(res.resource_name)
                infra_creator(client, res)
            except Exception as ex:
                logging.debug(
                    f"Error occurred while creating AWS resource: {res.resource_name} with config {res.config}")

def create_infra_all(environment, boto_clients):
    for resource in environment.resources:
        try:
            client = boto_clients.get(resource.resource_type)
            infra_creator = get_infra_creator(resource.resource_name)
            infra_creator(client, resource)
        except Exception as ex:
            logging.debug(
                f"Error occurred while creating AWS resource: {resource.resource_name} with config {resource.config}")

def delete_infra(env, boto_clients, resource):
    for res in env.resources:
        if resource == res.resource_name:
            try:
                client = boto_clients.get(res.resource_type)
                infra_deletion = get_infra_deletion(res.resource_name)
                infra_deletion(client, res)
            except Exception as ex:
                logging.debug(
                    f"Error occurred while creating AWS resource: {res.resource_name} with config {res.config}")


def delete_infra_all(environment, boto_clients):
    for resource in environment.resources:
        try:
            client = boto_clients.get(resource.resource_type)
            infra_deletion = get_infra_deletion(resource.resource_name)
            infra_deletion(client, resource)
        except Exception as ex:
            logging.debug(
                f"Error occurred while creating AWS resource: {resource.resource_name} with config {resource.config}")


def process_input(args):
    config_file = args.config_file
    environments, boto_clients = parse_input_config_file(config_file, args.env, args.delete, args.resource)
    if args.delete is not None:
        if args.delete != "All":
            for environment in environments:
                delete_infra(environment, boto_clients, args.delete)
        else:
            for environment in environments:
                delete_infra_all(environment, boto_clients)
    else:
        if args.resource != "All":
            for environment in environments:
                create_infra(environment, boto_clients, args.resource)
        else:
            # Invoke resource creation in AWS code below.
            for environment in environments:
                create_infra_all(environment, boto_clients)


def is_yaml_file(parser, arg):
    file_name, file_ext = arg.split('.')
    if file_ext not in ALLOWED_CONFIG_FILES:
        parser.error(
            f"Config file must be a yaml file, whereas given input file is of type {file_ext}")

    if not os.path.exists(arg):
        parser.error(
            f"File Not Found. The input config file does not exist - {arg}")

    return arg


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='AWS Resources command line utility.')

    parser.add_argument(
        '-f', '--config_file', type=lambda x: is_yaml_file(parser, x), required=True,
        help='Config file. Provide the path and file name of the config file.'
    )

    parser.add_argument(
        '-t', '-e', '--env', '--target', dest="env", type=str, default=None,
        help='Env name of the environment to spin up.'
    )

    parser.add_argument(
        '-r', '--resource', type=str, choices=ALLOWED_AWS_RESOURCES, default=ALL_SERVICES,
        help=(
            'Names of a particular AWS resource that you would like to create. '
            'Defaults to All services mentioned in the config file. '
            'We currently support only these resources - {}.'.format(
                ', '.join(ALLOWED_AWS_RESOURCES))
        )
    )

    parser.add_argument(
        '-d', '--delete', type=str, choices=ALL_RESOURCE_DELETE, default=None,
        help='Env name of the environment to spin down.'
    )

    args = parser.parse_args()

    process_input(args)
