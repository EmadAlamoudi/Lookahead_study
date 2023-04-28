#!/bin/sh

cur_PWD=${1}
IP=${2}
PORT=${3}
PYHTONFILE=${4}

cd ${cur_PWD}

echo "cur_PWD: $cur_PWD"
echo "IP: $IP"
echo "PORT: $PORT"
echo "PYHTONFILE: $PYHTONFILE"

# Source module
source ./load_module.sh

# Start the python script

python ${PYHTONFILE} --port ${PORT} --ip ${IP} > out.txt 2> err_${PORT}.txt

