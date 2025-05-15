from core.authentication.authentication import BasicAuthenticationHandler
from core.factory.register_mod import mod_registry

class ExamplePxyHandleAuthentication():
    basic_auth: BasicAuthenticationHandler

    def __init__(self, ):
        self.basic_auth = BasicAuthenticationHandler(
            username="username",
            password="password",
            mod_name=mod_registry["example_pxy"].name
        )
    

    def register(self) -> BasicAuthenticationHandler:
        return self.basic_auth

