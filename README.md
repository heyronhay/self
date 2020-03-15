# self

Self updating docker-based application

## Overview

Self is a docker-based CLI application that will update itself when it is run.  It is composed of two parts:

1. A docker-ized Python application that, as a demonstration, can perform various lookups from various APIs.  Python was used, but any language can be included.
1. `self` the wrapper script that passes arguments into the docker image when it runs.  This wrapper script is pulled from the docker image itself.

On every run, it will attempt to pull a new version from Docker Hub allowing for automatic updates.  Additionally, the wrapper script will self-update on a successful pull.

## Repository Tour

This repo makes use of Github actions (kept in the .github/workflows directory) to perform CI/CD.  Specifically, on any commit to `master`, the `buildandtest.yml` action is peformed, which in turn builds the docker image, and runs pytest against it.  On any release of self, the `buildandrelease.yaml` action is performed, which builds the docker image, tags it, and pushes it to Docker Hub.  The credentials for Docker Hub are stored in Github Secrets.

All building, tagging, pushing, and testing functionality is incorporated into a Makefile, with the following targets:

* build
* push
* login
* test
* build_and_test
* release

## Installation

Depending on your OS, perform one of the following sets of commands in a shell window.  This puts the wrapper script
into your current directory.  Make sure it is executable, and then move it into one of the directories in your PATH.

Linux/Mac:

    id=$(docker create heyronhay/self:latest); docker cp $id:/tmp/myapp/self.sh ./self; docker rm -v $id

Windows:

    docker create heyronhay/self:latest > temp.txt
    set /p ID=<temp.txt
    docker cp %ID%:/tmp/myapp/self.bat .
    docker rm -v %ID%

## Using

After installation, you can just use the `self` script, which is, itself, self-updating.

    self --help

## Local Debugging of Python application

You can either run pytest via docker and make:

    make build_and_test

or use Pipenv:

    # Run the first three commands on initial setup:
    pipenv --python 3.7         
    pipenv install
    pipenv run pip install -e .

    # Run this to actually test
    pipenv run pytest

## Critique of the docker approach to a self-updating application

### Upsides
* Multiple languages - anything that can run on your base OS image in your docker container can be put into it.
* Update facilities via Docker - standard, well used, well documented.  I used Docker Hub, but there are a number of hosting facilities for docker images.
* Complexity possible - can have different services running in the docker container that your application can make use of.  With tweaking of the wrapper script, you could have a long-running container going that has database services (Postgres, Redis, etc) or other third-party services.
* Contained datafiles - data files, configs, etc for an application can be contained inside the image, and moved around as needed without worrying how to clean up installs.
* Platform agnostic - other than the wrapper script, everything is in the docker image, and can be run on any platform that supports docker
* Amenable to container workflows - since the application is container based already, using it in various container environments is more straightforward (k8s, docker-compose, docker swarm, etc)
* Strangler pattern for refactoring - single point of entry can redirect to legacy scripts
* Security - using credentials for Docker Hub allows only those with access to pull the application.  Using another service could give more fine grained control (IAM in AWS docker registry, for instance)

### Downsides
* Need Docker - Not a big deal on Linux, but there are some maintenance issues with Mac/Windows due to the need to how docker is run (in a VM) on those platforms.
* Application bloat - the base docker image is around 100 MB compressed.  Not as big a deal in today's world, but still a minor issue.  After the first execution, though, the base OS will be cached and that generally won't change.
* Path issues - As is, the wrapper script uses the current working directory as a volume into the docker image.  However, this prevents access to files outside of the current path tree.  So `self ../file.txt` is unavailable to the application.  This can be solved by mapping the root volume of the host to the container, and then turning all relative paths into full paths in the wrapper script.  Doable, but clunky.  Probably the most serious limitation of this approach.
* Execution time - Overhead of running the docker image, minimal.
* No GUI - Technically you can get a GUI by using X-Windows, but that is clunky and requires installing extra software on Mac & Windows.  Could also run a web server and just have a webapp like Jupyter.

### Known Issues
* If `self` is in multiple locations, only one will be updates (docker pull gets the latest and updates the `self` that is executed, but no others).  Workaround is to compare wrapper version to version of wrapper inside the docker, and copy if different.
* No significant input sanitization or any real attempts to verify the inputs are well formatted
* Checks for docker, but lots of things could go wrong still.  There would like need to be several rounds of robustness development performed.  Although that is mostly with the wrapper, an advantage to using Docker for the main application is that robustness already exists.
* Can't access outside of directory command is executed in, can make a root volume, and translate paths in the self wrapper script
* Instead of always pulling from Docker to see if there is a new image, it would be nice if it checked the tag list and then determined from that if there was a new image, so the "updating" message could be displayed before the large download.
* When developing locally, changes to `self.sh` (or `self.bat`) can be overwritten if you don't build the docker image, since it tries to pull the latest, and if it is updated on the docker hub, it will pull the `self.sh` (or `self.bat`) out of the image again.
* Uses simple grep to determine if the docker pull is up to date, could use a more robust mechanism.
