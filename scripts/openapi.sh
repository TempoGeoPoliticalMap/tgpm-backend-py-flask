#!/bin/bash

# THIS SCRIPT SHOULD RUN FROM THE ROOT FOLDER

# remove old @generated folder
rm -rf src/@generated

# run open api generator
#npx openapi-generator-cli generate -i openapi/openapi.yaml -g python -o src/@generated --additional-properties=packageName=openapi_models
npx openapi-generator-cli generate -i openapi/openapi.yaml -g python-flask -o src/@generated --additional-properties=packageName=openapi_models


# clean up `src/@generated`
#rm -rf src/@generated/.github/
#rm -rf src/@generated/docs/
#rm -rf src/@generated/openapi_models/api/
#rm src/@generated/openapi_models/api_client.py
#rm src/@generated/openapi_models/api_response.py
#rm src/@generated/openapi_models/configuration.py
#rm src/@generated/openapi_models/exceptions.py
#rm src/@generated/openapi_models/py.typed
#rm src/@generated/openapi_models/rest.py
#rm -rf src/@generated/test/
#rm src/@generated/.gitignore
#rm src/@generated/.gitlab-ci.yml
#rm src/@generated/.openapi-generator-ignore
#rm src/@generated/.travis.yml
#rm src/@generated/git_push.sh
#rm src/@generated/pyproject.toml
#rm src/@generated/README.md
#rm src/@generated/requirements.txt
#rm src/@generated/setup.cfg
#rm src/@generated/setup.py
#rm src/@generated/test-requirements.txt
#rm src/@generated/tox.ini
#truncate -s 0 src/@generated/openapi_models/__init__.py

# formatter
black src/@generated/


