#!/bin/bash
export PYTHONWARNINGS='ignore'

# export PYTHONPATH=./python_translators
# python -m unittest discover -v -s ./tests/translators
python -m pytest

export PYTHONWARNINGS='default'
