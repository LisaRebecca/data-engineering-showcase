#!/bin/bash
rm data/connections.sqlite
rm data/ev_chargin_points_germany.sqlite
rm data/ev_chargin_points_per_district.sqlite
python3 ./project/data-pipeline.py