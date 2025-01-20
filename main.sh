#!/bin/bash

# Generate the site
python3 src/main.py

# Serve the site
cd public && python3 -m http.server 8888