import os
from hvac import Client


class SecretsV2():
    def __init__(self, client_token):
        if not os.getenv("VAULT_URL"):
            raise Exception("VAULT_URL is a mandatory env variable")
        else:
            self.vault_url = os.getenv("VAULT_URL")

        self.client = Client(url=self.vault_url, token=client_token)

        if not os.getenv("VAULT_SECRET_PATH"):
            raise Exception("VAULT_SECRET_PATH is a mandatory env variable")
        else:
            self.secret_path = os.getenv("VAULT_SECRET_PATH")

        if not os.getenv("ENV_VARIABLES_PATH"):
            raise Exception("ENV_VARIABLES_PATH is a mandatory env variable")
        else:
            self.ENV_VARIABLES_PATH = os.getenv("ENV_VARIABLES_PATH")

    def create_env_file(self):
        try:
            data = self.client.secrets.kv.v2.read_secret_version(path=self.secret_path)
            if data is None:
                raise Exception(self.secret_path+' is Invalid Path')
            else:
                f = open(self.ENV_VARIABLES_PATH, "w+")
                for i, j in data["data"]["data"].items():
                    f.write("export %s=\"%s\"\n" % (i, j))
                f.close()
            return True
        except Exception as e:
            print(e)
            return e


