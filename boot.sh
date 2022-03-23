#!/bin/bash
source venv/bin/activate
exec gunicorn -b :5000 app:app
