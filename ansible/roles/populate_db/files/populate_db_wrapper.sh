#!/bin/bash

source "{{ virtualenv_path }}/bin/activate"
cd "{{ project_source }}"
./populate_db.py --gendata --recalc_constraints --recalc_points
