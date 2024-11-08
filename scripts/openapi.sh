#!/bin/bash

# THIS SCRIPT SHOULD RUN FROM THE ROOT FOLDER

# remove old @generated folder
rm -rf src/main/@generated

# run open api generator
npx openapi-generator-cli generate -i openapi/openapi.yaml -g python-flask -o src/main/@generated --additional-properties=packageName=openapi_models

# replace updated openapi file with the original one
cp openapi/openapi.yaml src/main/@generated/openapi_models/openapi/openapi.yaml

# clean up `src/main/@generated`
rm -rf src/main/@generated/openapi_models/controllers/
rm -rf src/main/@generated/openapi_models/test/
rm src/main/@generated/openapi_models/__main__.py
rm src/main/@generated/openapi_models/encoder.py
rm src/main/@generated/.dockerignore
rm src/main/@generated/.gitignore
rm src/main/@generated/.openapi-generator-ignore
rm src/main/@generated/.travis.yml
rm src/main/@generated/Dockerfile
rm src/main/@generated/git_push.sh
rm src/main/@generated/README.md
rm src/main/@generated/requirements.txt
rm src/main/@generated/setup.py
rm src/main/@generated/test-requirements.txt
rm src/main/@generated/tox.ini


# formatter
black src/main/@generated/


