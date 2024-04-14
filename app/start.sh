#!/bin/bash
exec python app.py prod
exec python worker.py
