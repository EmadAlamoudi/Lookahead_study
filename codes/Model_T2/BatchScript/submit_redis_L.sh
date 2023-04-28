#!/bin/sh

cur_PWD=${1}
PORT=${2}

echo '#### cur_PWD= ####'${cur_PWD}
echo '#### PORT= ####'${PORT}

cd ${cur_PWD}

echo '#### This is the redis script job ####'

# Source module
source ./load_module.sh

# Start redis-worker
/home/ealamoodi/redis-stable/src/./redis-server --port ${PORT} --protected-mode no


