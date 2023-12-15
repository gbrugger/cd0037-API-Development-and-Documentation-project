#!/bin/bash
# backend
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=flaskr
docker start postgres_container_tests

# frontend Node.js>=17
export NODE_OPTIONS="--openssl-legacy-provider"