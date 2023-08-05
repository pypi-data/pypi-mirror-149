from cloudbuddy.aws_resources.resource_base import AWSResource
from cloudbuddy.constants import AWS_RESOURCE_ECS, AWS_RESOURCE_TYPE_ECS


class ECSResource(AWSResource):
    def __init__(self, config):
        super().__init__(config)
        self.resource_name = AWS_RESOURCE_ECS
        self.resource_type = AWS_RESOURCE_TYPE_ECS

        # List all required and optional vars
        self.required_fields = ['name', 'prefix', 'region']
        self.parse_config()
        self.check_required_fields()
        self.ecs_optional_params = getattr(self, 'ecs_optional_params', {})
