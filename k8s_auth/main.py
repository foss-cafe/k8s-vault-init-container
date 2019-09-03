import os
from hvac import Client


class GetAuthToken():
    def __init__(self):
        if not os.getenv("SERVICE_ACCOUNT_TOEKN_PATH"):
            self.k8s_service_account_token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        else:
            self.k8s_service_account_token_path = os.getenv("SERVICE_ACCOUNT_TOEKN_PATH")

        if not os.getenv("VAULT_ROLE"):
            raise Exception('VAULT_ROLE is a mandatory env variable')
        else:
            self.role = os.getenv("VAULT_ROLE")
        if not os.getenv("VAULT_URL"):
            raise Exception("VAULT_URL is a mandatory env variable")
        else:
            self.vault_url = os.getenv("VAULT_URL")

        self.client = Client(url=self.vault_url)

    def get_auth_token(self):
        try:
            service_account_token = open(self.k8s_service_account_token_path)
            jwt = service_account_token.read()
            data = self.client.auth_kubernetes(role=self.role, jwt=jwt)
            return data["auth"]["client_token"]
        except Exception as e:
            print(e)
        finally:
            service_account_token.close()


