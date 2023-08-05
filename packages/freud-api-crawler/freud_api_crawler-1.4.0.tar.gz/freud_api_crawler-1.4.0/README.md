[![PyPI version](https://badge.fury.io/py/freud-api-crawler.svg)](https://badge.fury.io/py/freud-api-crawler)
[![codecov](https://codecov.io/gh/freud-digital/freud_api_crawler/branch/master/graph/badge.svg?token=miLq3rRrcq)](https://codecov.io/gh/freud-digital/freud_api_crawler)

# Freud API Crawler

A client to interact with freud-net API


## install

* create a virtual environment and install the package with `pip install freud_api_crawler` 
* provide FRD_USER (freud-net username) and FRD_PW (freud-net password) as environment varibles, e.g. by
  * create a file called `env.secret` to store you freud-net api credentials
  * run `./set_env_variables.sh` 

### example `env.secret`

```
FRD_USER=username
FRD_PW=password
```

## usage

for how to use this package have a look into `./tests/test_freud_api_crawler.py` or check out the [frd-data-repo](https://github.com/freud-digital/frd-data)

## dev

* clone the repo
* create virtual env
* install dev-depenencies `pip install -r requirements_dev.txt`
* install the package (so you have the actual dependencies as well) `pip install -e .`

* run test with `coverage run -m pytest -v`
* create test-report `coverage report` or `coverage html`

## api-utils

### get work by title

https://www.freud-edition.net/jsonapi/node/werk?filter[field_titel.value]=%C3%9Cber%20den%20Traum
https://www.freud-edition.net/jsonapi/node/werk?filter[field_titel.value]=Über den Traum

### get manifestaion by node id

this ID can be taken from edit-url, e.g. https://www.freud-edition.net/node/51190/edit

https://www.freud-edition.net/jsonapi/node/manifestation?filter[drupal_internal__nid]=51190

https://www.freud-edition.net/jsonapi/node/manifestation?filter[drupal_internal__nid]=38946
https://www.freud-edition.net/node/38946/edit