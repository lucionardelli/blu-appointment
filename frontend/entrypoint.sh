#!/bin/sh
set -e

# Run npm install to make sure node_modules are up to date
npm install

# Execute the command passed to this script
exec "$@"
