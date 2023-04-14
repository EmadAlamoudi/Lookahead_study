#!/bin/sh

cur_PWD=${1}
IP=${2}
PORT=${3}
TIME=${4}
CPUSPERTASK=${5}

echo "cur_PWD: $cur_PWD"
echo "IP: $IP"
echo "PORT: $PORT"
echo "TIME: $TIME"
echo "PYHTONFILE: $PYHTONFILE"

cd ${cur_PWD}

# Source module
source ./load_module.sh

# Start redis-worker
/p/home/jusers/alamoodi1/juwels/.local/bin/abc-redis-worker  --host=${IP} --port ${PORT} --runtime ${TIME:0:2}h --processes 8


