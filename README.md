# SDR tools

Using the python script:
```
DESIGN='ni' SDR='sdr-01' JSON_PATH='sdrs.json' python design_change.py
```

Using the docker container:
```
docker run --rm -e DESIGN='ni' -e SDR='sdr-01' -e JSON_PATH='sdrs.json' samiemostafavi/change-sdr-design
```

Build the docker container:
```
docker build -t change-sdr-design .
docker tag change-sdr-design samiemostafavi/change-sdr-design
docker image push samiemostafavi/change-sdr-design
```
