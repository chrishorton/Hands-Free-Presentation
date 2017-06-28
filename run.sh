#!/usr/bin/env bash

if [ -e .snowboy_package ]
then
    python main.py
else
    python setup.py
fi