#!/bin/bash

if [[ -z "${F_DATA}" ]]; then
    python3 data_manip.py 
    export F_DATA=1;
fi
