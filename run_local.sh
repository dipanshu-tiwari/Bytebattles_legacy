#!/bin/bash

# Start Postgres
docker run --rm -d -p 5433:5432 -e POSTGRES_PASSWORD=passwd -v pgdata:/var/lib/postgresql/data postgres
echo "------------------- Postgres Started ---------------------"
sleep 3

# Start Redis
docker run --rm -d -p 5431:6379 redis
echo "------------------- Redis Started -----------------------"
sleep 3

# Open Judge Worker in new terminal
gnome-terminal -- bash -c "source venv/bin/activate && python3 -m judge_worker.judge_worker; exec bash"

# Open Result Worker in new terminal
gnome-terminal -- bash -c "source venv/bin/activate && python3 bytebattles/manage.py result_worker; exec bash"

# Open Django server in new terminal
gnome-terminal -- bash -c "source venv/bin/activate && python3 bytebattles/manage.py runserver 0.0.0.0:8000; exec bash"

