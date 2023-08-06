#! /bin/bash

GENERATOR=$1
if [ -z "$GENERATOR" ]; then
  GENERATOR=openapi-generator.jar
fi
if [ ! -f $GENERATOR ]; then
  >&2 echo "Generator jar not found."; exit 1
fi

INPUT=$2
if [ -z "$INPUT" ]; then
  INPUT=swagger.json
fi
if [ ! -f $INPUT ]; then
  >&2 echo "Swagger file not found."; exit 1
fi

VERSION=$3
if [ -z "$VERSION" ]; then
  VERSION=0.0.1
fi

OUTPUT=./

rm -rf $OUTPUT/docs $OUTPUT/bimdata_api_client $OUTPUT/test

# See https://openapi-generator.tech/docs/generators/typescript-fetch
# for a list of available additional properties.
java \
  -jar $GENERATOR generate \
  -g python \
  -i $INPUT \
  -o $OUTPUT \
  --additional-properties \
packageName=bimdata_api_client,\
projectName=bimdata-api-client,\
packageUrl=https://github.com/bimdata/python-api-client

exit 0
