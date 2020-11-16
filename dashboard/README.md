# fintools-ib-dashboard

A dashboard which shows graphs and auth status.

WORK IN PROGRESS.  
Run the install-dashboard.yml playbook.  
npm start  
Then go to  
http://localhost:8080



# Old: Quickstart
This was for when I would start this app from a shell script.  
It has now been converted do systemd services.


Run IB gateway, keepalive, and start the client.
```
./start.sh
npm start
```
Then auth in the browser window which automatically opened.

To kill, Ctrl+C.

Note: If some process was left hanging, `killall java; killall npm` and the one in `ps aux | grep keepalive.sh`.

Get list of NASDAQ stocks  
ftp://ftp.nasdaqtrader.com/symboldirectory/  
ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqlisted.txt
