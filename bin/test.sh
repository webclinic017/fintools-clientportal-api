#!/bin/bash
curl -sk "https://localhost:5000/v1/portal/iserver/marketdata/history?conid=209011562&period=1d&bar=1d" | jq '.'
