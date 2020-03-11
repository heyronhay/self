ifndef TAG
$(error The TAG variable is missing.)
endif

ifndef DOCKER_USER
$(error The DOCKER_USER variable is missing.)
endif

ifndef DOCKER_PASS
$(error The DOCKER_PASS variable is missing.)
endif

NAME   := heyronhay/self
IMG    := ${NAME}:${TAG}
LATEST := ${NAME}:latest
 
.PHONY: build push login all

build:
	@docker build -t ${IMG} .
	@docker tag ${IMG} ${LATEST}
 
push:
	@docker push ${NAME}
 
login:
	@echo ${DOCKER_PASS} | docker login -u ${DOCKER_USER} --password-stdin

all: login build push
