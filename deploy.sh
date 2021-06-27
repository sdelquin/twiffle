#!/bin/bash

# Commands to deploy project in production

git pull
pip install -r requirements.txt
supervisorctl restart twiffle
