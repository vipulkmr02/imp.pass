#!/bin/bash

CONTAINER_NAME="imp.pass"
PASSWD="root"

[[ "$#" == 1 ]] && PASSWD=$1

if [[ "$#" == 2 ]]; then
	CONTAINER_NAME=$1;
	PASSWD=$2
fi

echo "Container name: $CONTAINER_NAME"
echo "Password: $PASSWD"

if [[ "$CONTAINER_NAME" == $(docker ps | awk '{print $NF}' | grep -v "NAMES") ]]; then
	docker kill $CONTAINER_NAME > /dev/null
	docker rm $CONTAINER_NAME > /dev/null
	echo "Previous container killed & removed"
fi

docker run \
	--name "$CONTAINER_NAME" \
	-e MYSQL_ROOT_PASSWORD=$PASSWD \
	-p 3306:3306 \
	--restart=always \
	-d mysql > /dev/null

echo "New container created, $CONTAINER_NAME."
echo "run reset.sh to create schemas according to your project requirements."
