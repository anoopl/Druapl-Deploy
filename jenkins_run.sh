#!/bin/bash
profile=$1
#command=$2
GIT_REVISION=$2
fab -f fab_deploy.py $profile deploy:$GIT_REVISION

