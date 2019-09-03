import os
from k8s_auth.main import GetAuthToken
from kv2_auth.main import SecretsV2
get_tok = GetAuthToken()
token = get_tok.get_auth_token()
SecretsV2(client_token=token)
