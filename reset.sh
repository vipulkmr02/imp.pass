#/bin/bash

docker kill imp.pass
docker rm imp.pass


cmd='docker run --name=imp.pass --env MYSQL_ROOT_PASSWORD=root -p 3306:3306 --restart=always -d mysql '

output=$($cmd)

if [[ $? == 0 ]]; then
	echo -e "\033[1m[SUCCESS]\033[0m MySQL Container created"
	echo -e "Container ID: \033[1m${output::4}\033[0m"
else
	echo -e "\033[1m[FAILURE]\033[0m MySQL Container did not created"
	echo -e $? $output
fi

pushd src > /dev/null
echo -e "\033[1m[PYTHON-PROCCESS]\033[0m initializing zero.py"
python3 zero.py
echo -e "\033[1m[PYTHON-PROCCESS]\033[0m done zero.py"
echo -e "EXIT CODE: \033[1m$?\033[0m"

[[ -f .histories ]] && rm .histories
echo -e "\033[1m[DELETED]\033[0m user histories"
popd > /dev/null
