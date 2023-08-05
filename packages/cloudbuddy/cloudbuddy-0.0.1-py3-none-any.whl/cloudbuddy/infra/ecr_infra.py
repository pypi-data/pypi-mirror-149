from cloudbuddy.config import AWS_ACCOUNT_ID
from cloudbuddy.prettify_message import pprint
from botocore.exceptions import ClientError


def create_ecr(client, repo_name):
    try:
        pprint.pretty_print(
            f"Creating the ECR repository {repo_name} under the account {AWS_ACCOUNT_ID}", level="debug")
        client.create_repository(
            repositoryName=repo_name,
            tags=[
                {
                    "Key": "Name",
                    "Value": repo_name
                }
            ]
        )
        pprint.pretty_print(
            "Repository created... Please push the image to the ECR repo and rerun the script.", level="debug")

    except ClientError as ex:
        if ex.response["Error"]["Code"] == "ServerException":
            pprint.pretty_print(
                f"Server Exception while creating ecr repo: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(
                f"Invalid parameters passed while creating ecr repo: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "InvalidTagParameterException":
            pprint.pretty_print(
                f"Invalid Tag parameter while creating ecr repo: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "TooManyTagsException":
            pprint.pretty_print(
                f"Too many tags passed than expected while creating ecr repo: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "RepositoryAlreadyExistsException":
            pprint.pretty_print(
                f"Repository already exists: {ex}", level="error")
        else:
            pprint.pretty_print(
                f"Unexpected error occurred while creating ecr repo: {ex}")
        return False

    return True


def create_ecr_repo_operation(client, repo_name):
    create_repo_input = input(f"Would you like to create the repo with name "
                              f"{repo_name} in account {AWS_ACCOUNT_ID} - (Yes/No): ").upper()

    is_valid = False
    if create_repo_input == "YES":
        is_valid = create_ecr(client, repo_name)

    elif create_repo_input == "NO":
        pprint.pretty_print(f"The repository creation with name {repo_name} is cancelled. "
                            f"Please create the ECR repo and upload the image to the ECR Repo to proceed further",
                            level="info")

    else:
        pprint.pretty_print(f"Invalid Option. The repository creation with name {repo_name} is cancelled. "
                            f"Please create the ECR repo and upload the image to the ECR Repo to proceed further",
                            level="error")

    return is_valid


def check_ecr_image(client, repo_name, image_tag):
    try:
        image_list = client.describe_images(
            repositoryName=repo_name,
            imageIds=[
                {
                    "imageTag": image_tag
                },
            ],
            filter={
                "tagStatus": "TAGGED"
            }
        )
        if len(image_list.get("imageDetails")) > 0:
            pprint.pretty_print(
                f"Image exists with tag {image_tag} in ECR repository {repo_name}", level="info")
    except Exception as ex:
        if ex.response["Error"]["Code"] == "ServerException":
            pprint.pretty_print(f"Server Exception raised while checking for Image: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "ImageNotFoundException":
            pprint.pretty_print(
                f"The image with tag {image_tag} in ecr repo {repo_name} does not exist in the registry.",
                level="error")
            pprint.pretty_print("Please push the image and rerun the script", level="error")
        elif ex.response["Error"]["Code"] == "RepositoryNotFoundException":
            pprint.pretty_print(f"Repository not found while checking image: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(f"Invalid parameters are passed while checking for Images: {ex}", level="error")
        else:
            pprint.pretty_print(f"Unexpected Error. {ex}", level="error")
        return False

    return True


def check_ecr_repo_and_image(client, repo_name, image_tag):
    try:
        response_ecr = client.describe_repositories(repositoryNames=[repo_name])
        if len(response_ecr.get("repositories")) > 0:
            pprint.pretty_print(f"Repository already exists. ECR Repo name - {repo_name}", level="info")

    except Exception as ex:
        is_valid = False
        if ex.response["Error"]["Code"] == "RepositoryNotFoundException":
            pprint.pretty_print(f"The repository with name {repo_name} does not exist in the registry. Account {AWS_ACCOUNT_ID}",
                                level="error")
            is_valid = create_ecr_repo_operation(client, repo_name) 
        elif ex.response["Error"]["Code"] == "ServerException":
            pprint.pretty_print(f"Faced server side exception while checking for repo: {ex}", level="error")
        elif ex.response["Error"]["Code"] == "InvalidParameterException":
            pprint.pretty_print(f"Invalid params passed while checking repository: {ex}", level="error")
        else:
            pprint.pretty_print(f"Faced unexpected error while checking if repo exists: {ex}", level="error")
    else:
        is_valid = check_ecr_image(client, repo_name, image_tag)

    return is_valid
