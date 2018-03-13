#!/bin/bash
export PYTHONWARNINGS='ignore'

export PYTHONPATH=./python_translators
python -m unittest discover -v -s ./tests/translators

export PYTHONWARNINGS='default'