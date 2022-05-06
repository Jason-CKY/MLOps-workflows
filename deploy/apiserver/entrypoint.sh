#! /usr/bin/env sh
set -e

if [ -f /app/app/main.py ]; then
    DEFAULT_MODULE_NAME=app.main
elif [ -f /app/main.py ]; then
    DEFAULT_MODULE_NAME=main
fi
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

# set uvicorn LOG_CONFIG file
if [ -f /app/uvicorn_log_conf.json ]; then
    DEFAULT_UVICORN_CONF=/app/uvicorn_log_conf.json
elif [ -f /app/app/uvicorn_log_conf.json ]; then
    DEFAULT_UVICORN_CONF=/app/app/uvicorn_log_conf.json
else
    DEFAULT_UVICORN_CONF=/uvicorn_log_conf.py
fi
export UVICORN_CONF=${UVICORN_CONF:-$DEFAULT_UVICORN_CONF}


HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}
RELOAD=${RELOAD:-false}

# If there's a prestart.sh script in the /app directory or other path specified, run it before starting
PRE_START_PATH=${PRE_START_PATH:-/app/prestart.sh}
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else 
    echo "There is no script $PRE_START_PATH"
fi

# Start Uvicorn 
if [ -f $UVICORN_CONF ]; then
    if [ $RELOAD = "true" ]; then
        exec uvicorn --reload --host $HOST --port $PORT --log-config $UVICORN_CONF "$APP_MODULE"
    else
        exec uvicorn --host $HOST --port $PORT --log-config $UVICORN_CONF "$APP_MODULE"
    fi
else
    if [ $RELOAD = "true" ]; then
        exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
    else
        exec uvicorn --host $HOST --port $PORT --log-level $LOG_LEVEL "$APP_MODULE"
    fi
fi
