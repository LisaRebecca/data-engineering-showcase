# There should be at least one test case on the system-test level 
    # Executes your data pipeline
    # Validates that the output file(s) exist (but make sure the data pipeline creates them and you do not check them in)

#!/bin/bash
test -d venv || virtualenv venv
. venv/bin/activate; pip install -Ur requirements.txt
sh ./project/pipeline.sh
pytest project/system_tests.py
# alternatively: python3 ./project/system_tests.py