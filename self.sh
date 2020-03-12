#!/usr/bin/env bash

# Wrapper for a docker-based application.  Make sure this script is executable (chmod 755 self.sh)
# and put it in your PATH.

WRAPPER_VERSION="v0.0.8"

docker_error(){
    echo "ERROR: docker is not installed, or not in your PATH"
    exit 1
}

check_and_update_wrapper(){
    echo -n "Checking for latest version..."
    out=$(docker pull heyronhay/self:latest)
    fullpath=$(realpath $0)
    if [[ $out != *"up to date"* ]]; then
        echo -n "new version detected, updating..."
        id=$(docker create heyronhay/self:latest); docker cp $id:/tmp/myapp/self.sh $fullpath; docker rm -v $id > /dev/null

        echo "updated and using new version!"
        exec /bin/bash $fullpath $@
    else
        echo "up to date!"
    fi
}

# Check for docker on the system
which docker > /dev/null 2>&1 || docker_error

check_and_update_wrapper

docker run -it --rm --user $(id -u):$(id -g) -v "$PWD":/workdir -w /workdir heyronhay/self:latest self $@
