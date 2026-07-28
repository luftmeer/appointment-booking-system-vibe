#!/bin/sh
set -eu

attempt=1
max_attempts="${DATABASE_STARTUP_MAX_ATTEMPTS-10}"
retry_delay="${DATABASE_STARTUP_RETRY_DELAY-1}"

case "$max_attempts" in
    [1-9] | [1-9][0-9] | [1-9][0-9][0-9] | 1000) ;;
    *)
        echo "DATABASE_STARTUP_MAX_ATTEMPTS must be an integer from 1 through 1000" >&2
        exit 1
        ;;
esac

case "$retry_delay" in
    [0-9] | [1-9][0-9] | [12][0-9][0-9] | 300) ;;
    *)
        echo "DATABASE_STARTUP_RETRY_DELAY must be an integer from 0 through 300" >&2
        exit 1
        ;;
esac

until python -c 'import django; django.setup(); from django.db import connection; connection.ensure_connection(); connection.close()'
do
    if [ "$attempt" -ge "$max_attempts" ]; then
        echo "PostgreSQL did not become available after $max_attempts attempts" >&2
        exit 1
    fi

    echo "Waiting for PostgreSQL (attempt $attempt/$max_attempts)"
    attempt=$((attempt + 1))
    sleep "$retry_delay"
done

python manage.py migrate --noinput

exec "$@"
