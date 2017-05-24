#!/bin/bash
export PYTHONPATH=./python_translators
python -m unittest discover -v -s ./tests/translators
