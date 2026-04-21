#!/bin/bash
set -e

echo "Running database migrations..."
cd /app/models/db_schemes/minirag/
alembic upgrade head
cd /app

# هذا هو السطر اللي رح يشغل سيرفر الفاست إي بي آي ويمنع الكونتينر إنه يطفي
exec "$@"