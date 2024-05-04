#!/bin/bash

DOCKER_COMPOSE='./docker-compose.yml'

docker compose -f ${DOCKER_COMPOSE} build 
docker compose -f ${DOCKER_COMPOSE} up  -d