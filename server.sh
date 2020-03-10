uwsgi -s /tmp/fintools-ib.sock \
  --manage-script-name \
  --mount /yourapplication=myapp:__main__
