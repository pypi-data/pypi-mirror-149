from cloudbuddy.aws_resources.resource_base import AWSResource
from cloudbuddy.constants import AWS_RESOURCE_VPC, AWS_RESOURCE_TYPE_VPC


class VPCAccount(AWSResource):
    def __init__(self, config):
        super().__init__(config)
        self.resource_name = AWS_RESOURCE_VPC
        self.resource_type = AWS_RESOURCE_TYPE_VPC

        # List all required and optional vars
        self.required_fields = ['name', 'prefix', 'region']
        self.parse_config()
        self.check_required_fields()
