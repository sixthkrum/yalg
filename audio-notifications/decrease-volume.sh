#!/bin/bash

amixer set Master 1%- > /dev/null

bash $(dirname ${BASH_SOURCE})/helpers/show-volume-state.sh
