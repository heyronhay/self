#!/usr/bin/env bash

# Wrapper for a docker-based application.  Make sure this script is executable (chmod 755 self.sh)
# and put it in your PATH.

WRAPPER_VERSION="v0.1.2"

# Check to see if the given paramater exists in the parameter list
has_param() {
    local term="$1"
    shift
    for arg; do
        if [[ $arg == "$term" ]]; then
            return 0
        fi
    done
    return 1
}

docker_error(){
    echo "ERROR: docker is not installed, or not in your PATH"
    exit 1
}


check_and_update_wrapper(){
    echo -n "Checking for latest version..."
    out=$(docker pull heyronhay/self:latest)

    # Crossplatform way of getting the realpath, as OS X doesn't have the "realpath" command
    fullpath=$(python -c "import os; print(os.path.realpath('$0'))")
    if [[ $out != *"up to date"* ]]; then
        echo -n "new version detected, updating..."
        id=$(docker create heyronhay/self:latest); docker cp $id:/tmp/myapp/self.sh $fullpath; docker rm -v $id > /dev/null

        echo "updated and using new version!"
        exec /bin/bash $fullpath --no-update $@
    else
        echo "up to date!"
    fi
}

# Check for docker on the system
which docker > /dev/null 2>&1 || docker_error

if ! has_param '--no-update' "$@"; then
    check_and_update_wrapper
fi

for arg do
    shift
    [ "$arg" = "--no-update" ] && continue
    set -- "$@" "$arg"
done

docker run -it --rm --user $(id -u):$(id -g) -v "$PWD":/workdir -w /workdir heyronhay/self:latest self $@
