# fintools-ib

Replacement for fintools, using IB Client API beta.

# Quickstart
Run IB gateway, keepalive, and start the client.
```
./start.sh
```
Then auth in the browser window which automatically opened.

To kill, Ctrl+C.

Note: If some process was left hanging, `killall java; killall npm` and the one in `ps aux | grep keepalive.sh`.
