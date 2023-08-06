#!/bin/bash


if [[ -z "${SERVICE}" ]]; then
  echo "SERVICE env variable is not set"
  sh -c 'sleep infinity'
else
  echo "SERVICE=${SERVICE} env variable is set"
  if [[ "$SERVICE" == "reboot" ]]
  then
    echo "running reboot..."
    python3 /service/reboot/reboot.py
  elif [[ "$SERVICE" == "change_design" ]]
  then
    echo "running change_design..."
    python3 /service/change_design/change_design.py
  elif [[ "$SERVICE" == "start_mango" ]]
  then
    echo "running start_mango..."
    python3 /service/start_mango/start_mango.py
  elif [[ "$SERVICE" == "check_mango" ]]
  then
    echo "running check_mango..."
    python3 /service/check_mango/check_mango.py
  elif [[ "$SERVICE" == "config_mango_routes" ]]
  then
    echo "running config_mango_routes..."
    python3 /service/config_mango_routes/config_mango_routes.py
  fi
  sh -c 'sleep infinity'
fi


