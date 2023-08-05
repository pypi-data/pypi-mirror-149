from cloudbuddy.aws_resources.resource_base import AWSResource
from cloudbuddy.constants import AWS_RESOURCE_RDS, AWS_RESOURCE_TYPE_RDS


class RDSResource(AWSResource):
    def __init__(self, config):
        super().__init__(config)
        self.resource_name = AWS_RESOURCE_RDS
        self.resource_type = AWS_RESOURCE_TYPE_RDS

        # List all required and optional vars
        self.required_fields = ['name', 'prefix']
        self.parse_config()
        self.check_required_fields()
        self.rds_optional_params = getattr(self, 'rds_optional_params', {})
