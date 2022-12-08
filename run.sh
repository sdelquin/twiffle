#!/bin/bash
# Master script.

source ~/.pyenv/versions/twiffle/bin/activate
cd "$(dirname "$0")"
exec python main.py $@
