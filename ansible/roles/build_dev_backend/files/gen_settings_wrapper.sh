#!/bin/bash

source "{{ virtualenv_path }}/bin/activate"
cd "{{ project_source }}"
./tools/gen_settings.sh
