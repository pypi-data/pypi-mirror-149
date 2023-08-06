export SECRET_KEY=$(base64 /dev/urandom | head -c50)
export HOST=$(dig @resolver4.opendns.com myip.opendns.com +short)
export PRODUCTION=1
source ~/parsagon/venv/bin/activate
celery -A server worker -Q run_code
