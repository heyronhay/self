FROM python:3.7-slim-buster

LABEL authors="Ron Hay"

COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install -r /tmp/requirements.txt
COPY . /tmp/myapp/
RUN pip install /tmp/myapp
CMD self

