# SDR tools

## Change SDR Design

Using the python script:
```
DESIGN='ni' SDR='sdr-01' JSON_PATH='sdrs.json' python change-sdr-design.py
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
ROLE='sta' SDR='sdr-01' JSON_PATH='sdrs.json' MACADDR='40:d8:55:04:20:19' python start-mango-wifi.py
```

Using the docker container:
```
docker run -it --rm -e ROLE='sta' -e SDR='sdr-01' -e JSON_PATH='sdrs.json' -e MACADDR='40:d8:55:04:20:19' samiemostafavi/start-mango-wifi
```

Build the docker container:
```
docker build -t start-mango-wifi .
docker tag change-sdr-design samiemostafavi/start-mango-wifi
docker image push samiemostafavi/start-mango-wifi
```
