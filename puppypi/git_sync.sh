#!/bin/bash

# Change to your repository directory
cd /home/pi || exit 1

# Ensure we are on the correct branch
git fetch origin
git reset --hard origin/main
git pull origin main

exit 0
