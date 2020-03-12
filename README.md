# self
Self updating docker-based application

## Installation:
Copy one of the following commands depending on OS, paste into a shell, and hit enter.  This puts the wrapper script
into your current directory.  Make sure it is executable, and then move it into one of the directories in your PATH.

Linux/Mac:

    id=$(docker create heyronhay/self:latest); docker cp $id:/tmp/myapp/self.sh ./self; docker rm -v $id

Windows:

    docker create heyronhay/self:latest > temp.txt
    set /p ID=<temp.txt
    docker cp %ID%:/tmp/myapp/self.bat .
    docker rm -v %ID%

Upsides:
 Strangler pattern for refactoring - single point of entry can redirect to legacy scripts

Downsides:

Security:
 Using env variables
 Using github secrets

Improvements:
 * Can't acces outside of directory command is executed in, can make a root volume, and translate paths in the self wrapper script
