#!/bin/bash
API=https://localhost:5000/v1/portal
curl -sk "$API/tickle" >/dev/null
curl -sk "$API/sso/validate" >/dev/null
AUTHED=$(curl -sk "$API/iserver/auth/status" | jq -r '.authenticated')
if [[ $AUTHED == 'false' ]]; then
  curl -sk "$API/iserver/reauthenticate"
  echo -n
fi
