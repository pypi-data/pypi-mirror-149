from cerberus import Validator

# TODO: read up on Cerberus and extend functionality of this validator helper

class SolaceValidator:
    allow_unknown: bool = False
    require_all: bool = False

    def __init__(self, schema: dict):
        self.schema = schema
        self.validator = Validator()
    
    @property
    def errors(self):
        return self.validator.errors

    def __call__(self, data: dict):
        self.validator.allow_unknown = self.allow_unknown
        self.validator.require_all = self.require_all
        return self.validator.validate(data, self.schema)
