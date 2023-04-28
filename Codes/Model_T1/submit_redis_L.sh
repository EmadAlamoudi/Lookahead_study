#!/bin/sh

cur_PWD=${1}
PORT=${2}

echo '#### cur_PWD= ####'${cur_PWD}
echo '#### PORT= ####'${PORT}

cd ${cur_PWD}

echo '#### This is the redis script job ####'

# Start redis-worker
/p/project/fitmulticell/emad/redis-stable/src/./redis-server --port ${PORT} --protected-mode no


