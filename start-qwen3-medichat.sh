#!/bin/bash

if [ ! -d /mnt/temp ]; then
sudo /home/azureuser/tempDisk.sh ext4 /mnt/temp
sudo chown azureuser:azureuser -R /mnt/temp
fi

export AZCOPY_AUTO_LOGIN_TYPE=MSI

if [ ! -d /mnt/temp/qwen3-next-80b-q4ft/merged_16bit ]; then
azcopy copy "https://kyralfinetunedmodels.blob.core.windows.net/qwen3-next-80b-q4ft" /mnt/temp --recursive
fi

cd /home/azureuser/medichat-ai
docker-compose up -d