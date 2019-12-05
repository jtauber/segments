#!/bin/sh

isort constructors.py dclasses.py syllabification.py
black constructors.py dclasses.py syllabification.py
flake8 --max-line-length=88 constructors.py dclasses.py syllabification.py
mypy constructors.py dclasses.py syllabification.py
