#!/bin/sh

# Wrapper for a docker-based application.  Make sure this script is executable (chmod 755 self.sh)
# and put it in your PATH.

APPNAME="$(basename $0)"
WRAPPER_VERSION="v0.0.1"

docker_error(){
    echo "ERROR: docker is not installed, or not in your PATH"
    exit 1
}
# Check for docker on the system
which docker > /dev/null 2>&1 || docker_error

docker run -it --rm -v "$PWD":/workdir -w /workdir "heyronhay/self:latest" self $@
