#!/usr/bin/env bash

if ! [ -e .snowboy_path ]
then
    echo "Running setup..."
    python setup.py
fi
echo "Starting program..."
python main.py
