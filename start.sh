#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker run -d -p 9500:80 \
	--name=${app} \
	-v $PWD:/app ${app}
