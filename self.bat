:: Windows batch file wrapper for a docker-based application.  Make sure this script is executable
:: and put it in your PATH.

docker run -it --rm --user $(id -u):$(id -g) -v %CD%:/workdir -w /workdir heyronhay/self:latest self %*

