#!/bin/bash


if [[ -z "${SERVICE}" ]]; then
  echo "SERVICE env variable is not set"
  sh -c 'sleep infinity'
else
  echo "SERVICE=${SERVICE} env variable is set"
  if [[ "$SERVICE" == "reboot" ]]
  then
    sh -c 'python3 /service/reboot/reboot.py'
    sh -c 'sleep infinity'
  elif [[ "$SERVICE" == "change_design" ]]
  then
    sh -c 'python3 /service/change_design/change_design.py'
    sh -c 'sleep infinity'
  elif [[ "$SERVICE" == "start_mango" ]]
  then
    sh -c 'python3 /service/start_mango/start_mango.py'
    sh -c 'sleep infinity'
  elif [[ "$SERVICE" == "check_mango" ]]
  then
    sh -c 'python3 /service/check_mango/check_mango.py'
    sh -c 'sleep infinity'
  elif [[ "$SERVICE" == "config_mango_routes" ]]
  then
    sh -c 'python3 /service/config_mango_routes/config_mango_routes.py'
    sh -c 'sleep infinity'
  fi
fi


