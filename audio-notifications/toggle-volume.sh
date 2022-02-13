#!/bin/bash

amixer set Master toggle > /dev/null

bash $(dirname ${BASH_SOURCE})/helpers/show-volume-state.sh
