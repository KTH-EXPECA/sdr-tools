# SDR tools

Using the python script:
```
DESIGN='ni' SDR='sdr-01' JSON_PATH='sdrs.json' python design_change.py
```

Using the docker container:
```
```

Build the docker container:
```
sudo docker build -t change-sdr-design .
sudo docker tag change-sdr-design samiemostafavi/change-sdr-design
sudo docker image push samiemostafavi/change-sdr-design
```
