#!/bin/bash

files="$(find ./rpm_solver -type f | paste -sd " " -)"
python submit.py --provider gt --assignment $1 --files $files