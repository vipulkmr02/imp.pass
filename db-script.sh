#!/bin/bash

name="imp.pass"

if [[ "$name" == $(docker ps | awk '{print $NF}' | grep -v "NAMES") ]]
then
	docker kill $name
	docker rm $name
fi

docker run \
	--name "$name" \
	-e MYSQL_ROOT_PASSWORD=root \
	-p 3306:3306 \
	--restart=always \
	-d mysql

