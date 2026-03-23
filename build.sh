#!/bin/bash

PYTHON_CMD=$(command -v python3 || command -v python)

$PYTHON_CMD ladder_zip.py
mkdir -p ./build
unzip -o ./publish/Chance.zip -d ./build
