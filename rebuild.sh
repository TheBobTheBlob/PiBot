#!/bin/bash
# Script to rebuild the docker image and restart the container
sudo docker container stop bot
sudo docker container rm bot
sudo docker image rm discord-bot
git restore
git pull
sudo docker build -t discord-bot .
sudo docker run --env-file .env --name bot -d discord-bot
