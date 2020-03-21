#!/bin/bash
curl -sk --connect-timeout 2 "https://localhost:5000/v1/portal/iserver/marketdata/history?conid=209011562&period=1d&bar=1d" | jq '.'
