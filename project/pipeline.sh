#!/bin/bash
rm data/connections.sqlite
rm data/charging_points_germany.sqlite
rm data/charging_points_development.sqlite
python3 ./project/data-pipeline.py