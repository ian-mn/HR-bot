#!/bin/sh

gunicorn main:app --bind 0.0.0.0:8010 --workers 4 --worker-class uvicorn.workers.UvicornWorker