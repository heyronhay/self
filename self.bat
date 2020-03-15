:: Windows batch file wrapper for a docker-based application.  Make sure this script is executable
:: and put it in your PATH.
@echo off

docker pull heyronhay/self:latest > pull_output.txt
findstr /m "up to date" pull_output.txt
if NOT %errorlevel%==0 (
echo "Newer version found, updating!"
docker create heyronhay/self:latest > docker_id.txt
set /p ID=<docker_id.txt
docker cp %ID%:/tmp/myapp/self.bat temp.bat
docker rm -v %ID%
copy /Y "temp.bat" "%~f0" & %~f0
)

docker run -it --rm -v %CD%:/workdir -w /workdir heyronhay/self:latest self %*
