class AWSResource:
    def __init__(self, config={}):
        self.resource_name = "AWS Resource"
        self.resource_type = None
        self.config = config
        self.required_fields = []

    def parse_config(self):
        for var, value in self.config.items():
            setattr(self, var, value)

    def check_required_fields(self):
        for required_field in self.required_fields:
            if getattr(self, required_field) is None:
                attr_input = input(f"Please provide the value of required field. "
                                   f"Resource {self.resource_name} - {required_field}: ")
                setattr(self, required_field, attr_input)
