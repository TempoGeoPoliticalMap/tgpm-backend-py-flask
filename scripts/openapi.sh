#!/bin/bash

# THIS SCRIPT SHOULD RUN FROM THE ROOT FOLDER

# remove old @generated folder
rm -rf src/@generated

# run open api generator
#npx openapi-generator-cli generate -i openapi/openapi.yaml -g python -o src/@generated --additional-properties=packageName=openapi_models
npx openapi-generator-cli generate -i openapi/openapi.yaml -g python-flask -o src/@generated --additional-properties=packageName=openapi_models


# clean up `src/@generated`
rm -rf src/@generated/openapi_models/controllers/
rm -rf src/@generated/openapi_models/test/
rm src/@generated/openapi_models/__main__.py
rm src/@generated/openapi_models/encoder.py
rm src/@generated/openapi_models/typing_utils.py
rm src/@generated/openapi_models/util.py
rm src/@generated/.dockerignore
rm src/@generated/.gitignore
rm src/@generated/.openapi-generator-ignore
rm src/@generated/.travis.yml
rm src/@generated/Dockerfile
rm src/@generated/git_push.sh
rm src/@generated/README.md
rm src/@generated/requirements.txt
rm src/@generated/setup.py
rm src/@generated/test-requirements.txt
rm src/@generated/tox.ini


# formatter
black src/@generated/


