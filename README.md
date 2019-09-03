# Vault init Container 
### Setup Guide

```bash
$ minikube start 
$ vault server -dev -dev-listen-address=0.0.0.0:8200
```
### Once your vault is running in dev mode set the env variables for cli
```bash
$ export VAULT_ADDR=http://{Internal_IP}:8200
```
### Enable Kubernetes Authentication
```bash
$ vault auth enable kubernetes
```
### Update Kubernetes Auth Configs in Vault
```bash
vault write auth/kubernetes/config \
    kubernetes_host=https://{Minikube IP}:8443 \
    kubernetes_ca_cert=@{path to ca.cert file}
 ```
### Create Vault policy for 
 
 ```bash
$ cat <<EOF | vault policy write vault-demo-policy -
    path "sys/mounts" { capabilities = ["read"] }
    path "secret/data/demo/*" { capabilities = ["read"] }
    path "secret/metadata/demo/*" { capabilities = ["list"] }
  EOF 
```
### Create a Role in Vault for kubernetes authentication
 ```bash 
 vault write auth/kubernetes/role/vault-example-role \
    bound_service_account_names=vault-serviceaccount \
    bound_service_account_namespaces=default \
    policies=vault-demo-policy \
    ttl=1h
 ```
 **vault-example-role:** will be used for authenticating from k8s init container by using serviceaccount jwt token.
 
 **bound_service_account_names:** Serice account used to create your deployment, which will be bounded to vault role
 
 **bound_service_account_namespaces:** namespace where k8s serviceaccount created
 
 **policies:** policy for authorizing to access secrets from vault 
 
 **ttl:** TTL of client token.
 
### Create Some Demo Secrets 
```bash 
vault kv put secret/demo/most-used-password password=123456
vault kv put secret/demo/first one=1234567890 two=2345678901 three=jsdfhdsjfh
vault kv put secret/demo/second green=lantern poison=ivy
vault kv put secret/demo/greek/alpha philosopher=plato
vault kv put secret/demo/greek/beta god=zeus
vault kv put secret/demo/greek/gamma mountain=olympus
```
