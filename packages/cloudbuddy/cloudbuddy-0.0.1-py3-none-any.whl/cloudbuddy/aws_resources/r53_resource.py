from cloudbuddy.aws_resources.resource_base import AWSResource
from cloudbuddy.constants import AWS_RESOURCE_R53, AWS_RESOURCE_TYPE_R53


class R53Resource(AWSResource):
    def __init__(self, config):
        super().__init__(config)
        self.resource_name = AWS_RESOURCE_R53
        self.resource_type = AWS_RESOURCE_TYPE_R53

        # List all required and optional vars
        self.required_fields = ['name', 'prefix', 'region', 'domain', 'subdomain']
        self.parse_config()
        self.check_required_fields()