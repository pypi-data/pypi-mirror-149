class AltinnAuthClientConfig:
    def __init__(self,
                 maskinport_client_id: str,
                 keycloak_secret_path: str,
                 platform_environment: str,
                 altinn_base_url: str):
        self.maskinport_client_id = maskinport_client_id
        self.keycloak_secret_path = keycloak_secret_path
        self.platform_environment = platform_environment
        self.altinn_base_url = altinn_base_url
