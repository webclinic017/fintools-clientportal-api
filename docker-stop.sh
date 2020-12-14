#!/bin/sh
docker-compose down -v
docker system prune --force --volumes
