# Shopcloud SecretHub CLI

The SecretHub CLI provides the command-line interface to interact with the SecretHub API.

## install

```
$ pip install shopcloud_secrethub
```

### Usage


__Reading and writing secrets:__  

```sh
$ secrethub auth
$ secrethub read <secret-name>
$ secrethub write <secret-name> <value>
```


__Provisioning your applications with secrets:__  

Provision a template file

```sh
$ secrethub inject -i app.temp.yaml -o app.yaml

# app.temp.yaml
env_variables:
  ENV: {{ talk-point/test-repo/env }}
  SECRET_KEY: {{ talk-point/test-repo/secret_key }}

```

Provision to the environment

```sh
$ eval `secrethub printenv -i app.temp.yaml`

# app.temp.yaml
env_variables:
  ENV: {{ talk-point/test-repo/env }}
  SECRET_KEY: {{ talk-point/test-repo/secret_key }}

```

__in Code:__  

```py
from shopcloud_secrethub import SecretHub
hub = SecretHub(user_app="test-script", api_token='<TOKEN>')
hub.read('talk-point/test-repo/secret_key')
```

### Deploy to PyPi

```sh
$ pip3 install wheel twine
$ python3 setup.py sdist bdist_wheel
$ twine upload dist/* 
```