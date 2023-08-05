BUILD_AND_TEST_SH = """\
#!/bin/bash

# set image and container name for test
DOCKERFILE=Dockerfile
DEV_IMAGE=test-${PWD##*/}
CONTAINER_NAME=$DEV_IMAGE

# get empty port
read LOWER_PORT UPPER_PORT < /proc/sys/net/ipv4/ip_local_port_range
while :
do
        TEST_PORT="`shuf -i ${LOWER_PORT}-${UPPER_PORT} -n 1`"
        ss -lpn | grep -q ":$TEST_PORT " || break
done
echo $TEST_PORT

# build
echo build '${DEV_IMAGE}'...
docker build -t ${DEV_IMAGE} . -f ${DOCKERFILE}
docker run --rm -d -p ${TEST_PORT}:8080 --name ${CONTAINER_NAME} ${DEV_IMAGE}

# test (remove "| jq" if jq is not installed)
curl -XPOST "http://localhost:${TEST_PORT}/2015-03-31/functions/function/invocations" -d '{"input1": "value1", "input2": "value2"}' | jq

# stop and remove test container
docker stop ${CONTAINER_NAME}
"""
