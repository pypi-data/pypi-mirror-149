export SECRET_KEY=$(base64 /dev/urandom | head -c50)
export HOST=$(dig @resolver4.opendns.com myip.opendns.com +short)
export PRODUCTION=1
source ~/parsagon/venv/bin/activate
daphne -b 127.0.0.1 -p 8000 server.asgi:application
