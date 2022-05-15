#!/bin/bash

# remove old @generated folder
rm -rf src/@generated

# run open api generator
npx openapi-generator-cli generate -i openapi/openapi.yaml -g python-flask -o src/@generated
