#!/bin/bash

# Wrapper for a docker-based application.  Make sure this script is executable (chmod 755 self.sh)
# and put it in your PATH.

WRAPPER_VERSION="v0.0.8"

docker_error(){
    echo "ERROR: docker is not installed, or not in your PATH"
    exit 1
}

check_and_update_wrapper(){
    out=$(docker pull heyronhay/self:latest)

    if [[ $out != *"up to date"* ]]; then    
        id=$(docker create heyronhay/self:latest); docker cp $id:/tmp/myapp/self.sh ./self; docker rm -v $id > /dev/null

        exec /bin/bash self $@
    fi
}

# Check for docker on the system
which docker > /dev/null 2>&1 || docker_error

check_and_update_wrapper

docker run -it --rm --user $(id -u):$(id -g) -v "$PWD":/workdir -w /workdir heyronhay/self:latest self $@
