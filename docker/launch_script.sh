#Launching MongoDB on localhost:27017

docker compose -f mongo_compose.yml up

#There is a mongo express ready to see the databases http://localhost:8081/

#FRONT API BUILDING
docker-compose -f .\front_api_compose.yml build
docker-compose -f .\front_api_compose.yml up

docker run --name my-redis -p 6379:6379 -d redis