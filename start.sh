#!/bin/bash

env_name="agenta"

if conda env list | grep -q -E "\b$env_name\b"; then
    conda activate agenta
else
    conda create -n $env_name python=3.10 -y
    conda activate agenta
fi

pip install -U agenta

docker compose -f docker-compose.yml up -d