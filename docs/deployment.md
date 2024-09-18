# Deployment

## Ubuntu Server Deployment

Follow DigitalOcean [tutorial](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu), with the following:



## Celery Deployment

On a Linux Ubuntu 22.04 LTS server, this is the configuration of Celery and Celery Beat with `systemd`, following most of the instructions in the [Daemonization guide](https://docs.celeryq.dev/en/stable/userguide/daemonizing.html#daemon-systemd-generic) of Celery.

- **Note**: this assumes that Redis is installed (`sudo apt install redis-server`) and all the Python packages in `requirements.txt`. It is possible to check if Redis is running with `sudo systemctl is-enabled redis-server`.

Configuring Celery as a system service. Preliminaries:

- The Django project is in `/home/bucr/screens`
- The virtual environment is in `/home/bucr/screens/screensenv/bin`
- The user is `bucr` and belongs to the group `bucr`

The environment variables are located in the file `/etc/conf.d/celery`, as shown below.

```ini title="/etc/conf.d/celery"
# Name of nodes to start
CELERYD_NODES="w1"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/home/bucr/screens/screensenv/bin/celery"

# App instance to use
CELERY_APP="screens"

# How to call manage.py
CELERYD_MULTI="multi"

# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=300 --concurrency=1"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/var/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"

# Celery Beat
CELERYBEAT_SCHEDULER="django_celery_beat.schedulers:DatabaseScheduler"
CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
```

Notes:

- Concurrency is set to 1 because current servers have single CPU(s), thread(s) per core and core(s) per socket.
- The directories `/var/run/celery/` and `/var/log/celery/` for the PID and LOG files, respectively, must first be created when configuring Celery. So:

```bash
sudo mkdir -p /var/run/celery/
sudo mkdir -p /var/log/celery/
```

- Now the user and group `bucr:bucr` need permissions for those directories:

```bash
sudo chown bucr:bucr /var/run/celery/
sudo chown bucr:bucr /var/log/celery/
```

- The PID file and log file must be created on each reboot with the following configuration, where `bucr bucr` is the user and group and `0755` are the permissions.

```ini title="/etc/tmpfiles.d/celery.conf"
d /run/celery 0755 bucr bucr -
d /var/log/celery 0755 bucr bucr -
```

### Celery Worker

This process is configured below.

```ini title="/etc/systemd/system/celery.service"
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=bucr
Group=bucr
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/home/bucr/screens/
RuntimeDirectory=celery
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" \
    $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} \
    --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" \
    $CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target
```

Relevant `systemctl` commands:

- On every change to this file: `sudo systemctl daemon-reload`
- To start: `sudo systemctl start celery`
- To stop: `sudo systemctl stop celery`
- To check status: `sudo systemctl status celery`
- To allow execution on reboot: `sudo systemctl enable celery`
- Others: `restart`/`reload`/`is-enabled`/`disable`

### Celery Beat

This process is configured below.

- **Note**: the periodic tasks are configured in the Django admin panel, thanks to the package `django-celery-beat`, and as configured here with `--scheduler` as `django_celery_beat.schedulers:DatabaseScheduler`.

```ini title="/etc/systemd/system/celerybeat.service"
[Unit]
Description=Celery Beat Service
After=network.target celery.service

[Service]
Type=simple
User=bucr
Group=bucr
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/home/bucr/screens/
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat \
    --pidfile=${CELERYBEAT_PID_FILE} \
    --logfile=${CELERYBEAT_LOG_FILE} \
    --loglevel=${CELERYD_LOG_LEVEL} \
    --scheduler ${CELERYBEAT_SCHEDULER}'
Restart=always

[Install]
WantedBy=multi-user.target
```

Relevant `systemctl` commands:

- On every change to this file: `sudo systemctl daemon-reload`
- To start: `sudo systemctl start celerybeat`
- To stop: `sudo systemctl stop celerybeat`
- To check status: `sudo systemctl status celerybeat`
- To allow execution on reboot: `sudo systemctl enable celerybeat`
- Others: `restart`/`reload`/`is-enabled`/`disable`

## Daphne Deployment

For using Channels and WebSockets, it is necessary to configure the Daphne server.

```init title="/etc/systemd/system/daphne.service" hl_lines="9"
[Unit]
Description=WebSocket Daphne Service
After=network.target

[Service]
User=bucr
Group=www-data
WorkingDirectory=/home/bucr/screens
ExecStart=/home/bucr/screens/screensenv/bin/daphne -p 8001 screens.asgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Relevant `systemctl` commands:

- On every change to this file: `sudo systemctl daemon-reload`
- To start: `sudo systemctl start daphne`
- To stop: `sudo systemctl stop daphne`
- To check status: `sudo systemctl status daphne`
- To allow execution on reboot: `sudo systemctl enable daphne`
- Others: `restart`/`reload`/`is-enabled`/`disable`

It is necessary to allow execution on reboot with `sudo systemctl enable daphne`.

Now, for Nginx to proxy pass to Daphne, the following is needed:

```init title="/etc/nginx/sites-available/screens" hl_lines="15-20"
server {
    listen 80;
    server_name pantallas.bucr.digital;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/bucr/screens;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }

    location /ws/ {
        proxy_pass http://localhost:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

}
```

## Updating the repository

When making changes to the repository... `git pull`...

```bash
sudo nano restart_services.sh
```

where

```bash
#!/bin/bash

sudo systemctl restart celery
sudo systemctl restart celerybeat
sudo systemctl restart daphne
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

and make executable with

```bash
sudo chmod +x restart_services.sh
```

and then execute

```bash
./restart_services.sh
```
