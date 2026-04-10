#!/bin/bash
set -e

BRANCH="master"
PROTOS_URL="https://storage.googleapis.com/noon-toolbox/perm/partner-integration-protos/swagger/partner_integration_protos-swagger-${BRANCH}.tar.gz"

TARGET_DIR="openapi/swagger"
TEMP_DIR="temp_swagger"

echo "--- Syncing Swagger Assets (External) ---"

mkdir -p "$TARGET_DIR"
mkdir -p "$TEMP_DIR"

echo "Downloading from noon-toolbox..."
curl -sSL "$PROTOS_URL" | tar -xz -C "$TEMP_DIR"

echo "Cleaning old files and updating $TARGET_DIR..."
# The :? is a safety check to ensure TARGET_DIR isn't empty before running rm -rf
rm -rf "${TARGET_DIR:?}"/*
cp -r "$TEMP_DIR"/. "$TARGET_DIR/"

# 4. Cleanup
rm -rf "$TEMP_DIR"

echo "Assets synced to $TARGET_DIR"
