import os
from k8s_auth.main import GetAuthToken
from kv2_auth.main import SecretsV2
print("Initiated")
get_tok = GetAuthToken()
token = get_tok.get_auth_token()
print("Got the token")
print(token)
SecretsV2(client_token=token).create_env_file()
print("Env file written successfully")
