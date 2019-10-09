#!/bin/bash

function cleanup() {
  echo EXITTING $PID1
  kill $(ps -o pid= --ppid $PID1 $PID2)
  exit 0
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
echo "STARTED KEEPALIVE ($PID2)"
trap cleanup INT
while true; do
  VAL=$(curl -sk \
    --connect-timeout 2 \
    --max-time 2 \
    https://localhost:5000/v1/portal/iserver/auth/status)
  if [[ $(echo $VAL | jq '.statusCode') == 401 ]]; then
    echo /auth/status: $VAL
  fi
  if [[ "$(echo $VAL | jq '.authenticated')" == "true" ]]; then
    break
  fi
  sleep 1
done
echo Authenticated
while true; do
  echo /sso/validate
  VAL=$(curl -sk https://localhost:5000/v1/portal/sso/validate | jq '.')
  echo $VAL
  sleep 60
done
