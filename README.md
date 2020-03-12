# self
Self updating docker-based application

## Installation:
Depending on your OS, perform one of the following sets of commands in a shell window.  This puts the wrapper script
into your current directory.  Make sure it is executable, and then move it into one of the directories in your PATH.

Linux/Mac:

    id=$(docker create heyronhay/self:latest); docker cp $id:/tmp/myapp/self.sh ./self; docker rm -v $id

Windows:

    docker create heyronhay/self:latest > temp.txt
    set /p ID=<temp.txt
    docker cp %ID%:/tmp/myapp/self.bat .
    docker rm -v %ID%

Upsides:
* Multiple languages - anything that can run on your base OS image in your docker container can be put into it.
* Update facilities via Docker - standard, well used, well documented.  I used Docker Hub, but there are a number of hosting facilities for docker images.
* Complexity possible - can have different services running in the docker container that your application can make use of.  With tweaking of the wrapper script, you could have a long-running container going that has database services (Postgres, Redis, etc) or other third-party services.
* Contained datafiles - data files, configs, etc for an application can be contained inside the image, and moved around as needed without worrying how to clean up installs.
* Platform agnostic - other than the wrapper script, everything is in the docker image, and can be run on any platform that supports docker
* Amenable to container workflows - since the application is container based already, using it in various container environments is more straightforward (k8s, docker-compose, docker swarm, etc)
* Strangler pattern for refactoring - single point of entry can redirect to legacy scripts

Downsides:
* Need Docker - Not a big deal on Linux, but there are some maintenance issues with Mac/Windows due to the need to how docker is run (in a VM) on those platforms.
* Application bloat - the base docker image is around 100 MB compressed.  Not as big a deal in today's world, but still a minor issue.  After the first execution, though, the base OS will be cached and that generally won't change.
* Path issues - As is, the wrapper script uses the current working directory as a volume into the docker image.  However, this prevents access to files outside of the current path tree.  So `self ../file.txt` is unavailable to the application.  This can be solved by mapping the root volume of the host to the container, and then turning all relative paths into full paths in the wrapper script.  Doable, but clunky.  Probably the most serious limitation of this approach.
* Execution time - Overhead of running the docker image, minimal.
* No GUI - Technically you can get a GUI by using X-Windows, but that is clunky and requires installing extra software on Mac & Windows.  Could also run a web server and just have a webapp like Jupyter.


Security:
* Using env variables
* Using github secrets

Improvements:
* Can't access outside of directory command is executed in, can make a root volume, and translate paths in the self wrapper script
