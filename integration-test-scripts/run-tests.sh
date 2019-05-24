#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

CONFIG_TAG="local"

export PYTHONPATH=../testing-tools

function execute_test
{
    local TEST_FILE=$1

    echo -e "\n${RED}start run test: $TEST_FILE${NC}\n"
    python3 $TEST_FILE $CONFIG_TAG
    if [ "$?" -ne 0 ]; then
        echo -e "\n${RED}failed finishing test: $TEST_FILE${NC}\n"
        break
    else
        echo -e "\n${RED}finishing test: $TEST_FILE${NC}\n"
    fi
}

if [ "$#" == 1 ]; then
    CONFIG_TAG=$1
fi

if [ "$#" == 2 ]; then
    CONFIG_TAG=$1
    execute_test $2
else
    for i in test_*.py; do
        execute_test $i
        sleep 0.5
    done

fi

