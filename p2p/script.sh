#!/bin/bash

docker rm -f `docker ps -aq`
docker rmi p2p_image

docker build -t p2p_image .

docker run -d --name bootstrap --network p2p_net --ip 172.20.10.40 p2p_image
docker run -d --name node_1 --network p2p_net --ip 172.20.10.60 p2p_image
docker run -d --name node_2 --network p2p_net --ip 172.20.10.70 p2p_image
docker run -d --name node_3 --network p2p_net --ip 172.20.10.80 p2p_image
