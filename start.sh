#!/bin/bash

function cleanup() {
  echo EXITTING $PID1 $PID2
  kill $(ps -o pid= --ppid $PID1 $PID2)
}

function keepalive() {
  while true; do
    echo `date`
    echo /auth/status
    curl -sk https://localhost:5000/v1/portal/iserver/auth/status | jq &
    echo /sso/validate
    curl -sk https://localhost:5000/v1/portal/sso/validate | jq &
    sleep 60
  done
}

pushd /home/konrad/Apps/IB/betaAPI
./bin/run.sh root/conf.yaml &
PID1=$!
echo "STARTED GATEWAY ($PID1)"
chromium https://localhost:5000 &
popd
keepalive &
PID2=$!
echo "STARTED KEEPALIVE ($PID2)"
trap cleanup INT
npm start
cleanup
