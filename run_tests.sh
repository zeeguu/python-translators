#!/bin/bash
export PYTHONPATH=./translators
python -m unittest discover -v -s ./tests/translators
