#!/bin/bash

# THIS SCRIPT SHOULD RUN FROM THE ROOT FOLDER

source config.env

# remove old @generated folder
rm -rf src/main/@generated

# run open api generator
openapi-generator-cli generate \
  -i "https://raw.githubusercontent.com/TempoGeoPoliticalMap/tgpm-openapi/${SPEC_SHA}/openapi.bundled.yaml" \
  -g python-flask \
  -o src/main/@generated \
  --additional-properties=packageName=openapi_models

# Post-process generated openapi.yaml:
#   1. Remove x-openapi-router-controller extensions (VersionedResolver handles routing)
#   2. Redirect x-bearerInfoFunc to our own no-op security controller
python3 - <<'PYEOF'
import re

path = "src/main/@generated/openapi_models/openapi/openapi.yaml"
with open(path) as f:
    content = f.read()

# Remove x-openapi-router-controller lines (VersionedResolver handles routing)
content = re.sub(r"[ \t]*x-openapi-router-controller:.*\n", "", content)

# Remove global security block (auth is handled at infrastructure level)
content = re.sub(r"^security:\n(- \w+:.*\n)+", "", content, flags=re.MULTILINE)

# Remove x-bearerInfoFunc extension lines
content = re.sub(r"[ \t]*x-bearerInfoFunc:.*\n", "", content)

with open(path, "w") as f:
    f.write(content)
print("openapi.yaml post-processed successfully")
PYEOF

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


# Post-process base_model.py:
#   to_dict() must use attribute_map values as JSON keys so models serialise
#   to camelCase (e.g. pageSize, totalItems) rather than snake_case.
#   The generator always emits snake_case keys; this one-line fix overrides that.
python3 - <<'PYEOF'
import re

path = "src/main/@generated/openapi_models/models/base_model.py"
with open(path) as f:
    content = f.read()

# Replace `result[attr] = ...` with `result[key] = ...` after inserting the key lookup
old = "        for attr in self.openapi_types:\n            value = getattr(self, attr)"
new = "        for attr in self.openapi_types:\n            key = self.attribute_map.get(attr, attr)\n            value = getattr(self, attr)"
content = content.replace(old, new)

# Replace every result[attr] assignment with result[key]
content = re.sub(r"result\[attr\]", "result[key]", content)

with open(path, "w") as f:
    f.write(content)
print("base_model.py post-processed successfully")
PYEOF

# formatter
black src/main/@generated/


