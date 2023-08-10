#!/usr/bin/env bash

set -e
set -o pipefail

SNAPSHOT="${SNAPSHOT:-$(date +%Y%m%d%H%M)}"
DIST_DIR="${DIST_DIR:-$(pwd)/dist}"
BASE_VERSION="$(cat version.txt)"
DUET3D_PLUGIN_VERSION="$BASE_VERSION-SNAPSHOT.$SNAPSHOT"
BUNDLE_ID=PrintNannyDuetPlugin

TARGET_DIR="${DIST_DIR}/$BUNDLE_ID"

echo "Creating Duet3D plugin release: $TARGET_DIR"

mkdir -p "$TARGET_DIR"

DUET3D_PLUGIN_VERSION="$DUET3D_PLUGIN_VERSION" j2 plugins/duet3d/plugin.j2 -o "$TARGET_DIR/plugin.json"
cp -r plugins/duet3d/dsf "$TARGET_DIR/dsf"
cp -r plugins/duet3d/src "$TARGET_DIR/src"
