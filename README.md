# SDR tools

## Reboot SDR

```
SDR='sdr-02' JSON_PATH='sdrs.json' python reboot/reboot.py
```

## Change SDR Design

Using the python script:
```
DESIGN='ni' SDR='sdr-01' JSON_PATH='sdrs.json' python change_design/change_design.py
```

Using the docker container:
```
docker run -it --rm -e DESIGN='ni' -e SDR='sdr-01' -e JSON_PATH='sdrs.json' samiemostafavi/change-sdr-design
```

Build the docker container:
```
docker build -t change-sdr-design .
docker tag change-sdr-design samiemostafavi/change-sdr-design
docker image push samiemostafavi/change-sdr-design
```

## Start Mango WiFi

Using the python script:
```
DESIGN='mango' SDR='sdr-02' SIDE='ap' CONFIG='{"mac_addr":"40:d8:55:04:20:12"}' JSON_PATH='sdrs.json' python start_mango/start_mango.py
```
```
DESIGN='mango' SDR='sdr-01' SIDE='sta' CONFIG='{"mac_addr":"40:d8:55:04:20:19"}' JSON_PATH='sdrs.json' python start_mango/start_mango.py
```

## Configure Mango Routing

```
```
