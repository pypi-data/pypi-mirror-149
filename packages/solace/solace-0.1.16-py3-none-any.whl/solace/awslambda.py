""" a simple wrapper to provide Lambda support, powered by Mangum. """
from mangum import Mangum
from solace import Solace

class SolaceLambda:
    api_gateway_base_path: str = "/"

    def __init__(self, app: Solace):
        self.app = app

    def __call__(self):
        return Mangum(
            self.app, 
            lifespan="off",
            api_gateway_base_path = self.api_gateway_base_path
        )
