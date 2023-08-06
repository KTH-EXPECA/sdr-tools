#!/bin/bash


if [[ -z "${SERVICE}" ]]; then
  echo "SERVICE env variable is not set"
  sh -c 'sleep infinity'
else
  echo "SERVICE=${SERVICE} env variable is set"
  if [[ "$SERVICE" == "reboot" ]]
  then
    python3 /service/reboot/reboot.py
  elif [[ "$SERVICE" == "change_design" ]]
  then
    python3 /service/change_design/change_design.py
  elif [[ "$SERVICE" == "start_mango" ]]
  then
    python3 /service/start_mango/start_mango.py
  elif [[ "$SERVICE" == "check_mango" ]]
  then
    python3 /service/check_mango/check_mango.py
  elif [[ "$SERVICE" == "config_mango_routes" ]]
  then
    python3 /service/config_mango_routes/config_mango_routes.py
  fi
  sh -c 'sleep infinity'
fi


