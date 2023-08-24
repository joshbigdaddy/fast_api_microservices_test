#!/bin/bash
#Killing all possible containers
docker kill $(docker ps -q)
#Launching MongoDB on localhost:27017

docker compose -f mongo_compose.yml up -d

#There is a mongo express ready to see the databases http://localhost:8081/
#INGESTION CONTAINERS -------------------------------------------------------
##INGEST_USD CONTAINER
docker-compose -f .\usd_ingest_api_compose.yml build
docker-compose -f .\usd_ingest_api_compose.yml up

#INGEST_ASSETS CONTAINER
docker-compose -f .\asset_ingest_compose.yml build
docker-compose -f .\asset_ingest_compose.yml up

##FRONT API ----------------------------------------------------------------
#Redis Server UP handling cache for the processes
docker rm my-redis
docker run --name my-redis -p 6379:6379 -d redis
#FRONT API BUILDING
docker-compose -f .\front_api_compose.yml build
docker-compose -f .\front_api_compose.yml up
