#!/bin/bash

if [[ "$SERVICE" == "reboot" ]]
then
  sh -c 'python3 /service/reboot/reboot.py'
elif [[ "$SERVICE" == "change_design" ]]
then
  sh -c 'python3 /service/change_design/change_design.py'
elif [[ "$SERVICE" == "start_mango" ]]
then
  sh -c 'python3 /service/start_mango/start_mango.py'
elif [[ "$SERVICE" == "config_mango_routes" ]]
then
  sh -c 'python3 /service/config_mango_routes/config_mango_routes.py'
fi
