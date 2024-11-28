docker ps


docker stop "imagem" 
docker rm "imagem"

⮞  docker run -it --name app_client --rm -e SERVER_IP=172.19.0.2 app_client

docker inspect "imagem"

rogan72's PI/
⮞  docker build --no-cache -t app_client -f docker/Dockerfile.client .


⮞  docker run --network=mynetwork --name app_server -p 50051:50051 app_server

⮞  docker build --no-cache -t app_server -f docker/Dockerfile.server .
