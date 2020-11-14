#!/bin/bash
API=https://localhost:5000/v1/portal
CURL="curl -sk --connect-timeout 2"
$CURL "$API/tickle" >/dev/null
$CURL "$API/sso/validate" >/dev/null
AUTHED=$($CURL "$API/iserver/auth/status" | jq -r '.authenticated')
if [[ $AUTHED == 'false' || $AUTHED == '' ]]; then
  echo Reauthenticating
  $CURL "$API/iserver/reauthenticate"
  echo -n
fi
