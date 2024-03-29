#!/bin/sh

export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

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
/home/ealamoodi/.local/bin/abc-redis-worker  --host=${IP} --port ${PORT} --runtime ${TIME:0:2}h --processes ${CPUSPERTASK} --daemon false




