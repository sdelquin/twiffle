#!/bin/bash
# Master script.

source ~/.virtualenvs/twiffle/bin/activate
cd "$(dirname "$0")"
exec python main.py $@
