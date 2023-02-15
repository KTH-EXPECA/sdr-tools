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

AP:
```
DESIGN='mango' SDR='sdr-02' SIDE='ap' CONFIG='{"mac_addr":"40:d8:55:04:20:12"}' JSON_PATH='sdrs.json' python start_mango/start_mango.py
```
STA:
```
DESIGN='mango' SDR='sdr-01' SIDE='sta' CONFIG='{"mac_addr":"40:d8:55:04:20:19"}' JSON_PATH='sdrs.json' python start_mango/start_mango.py
```

## Configure Mango Routing

AP:
```
SDR='sdr-02' SIDE='ap' JSON_PATH='sdrs.json' CONFIG='{"protocol":"udp","server":{"ip":"10.30.1.251","port":"50000"},"ap":{"server_port":"50500","sta_port":"50000"},"sta":{"mac_addr":"40:d8:55:04:20:19","ip":"192.168.11.10","ap_port":"50500"}}' python config_mango_routes/config_routes.py
```
STA:
```
SDR='sdr-01' SIDE='sta' JSON_PATH='sdrs.json' CONFIG='{"protocol":"udp","client":{"ip":"10.30.1.252","port":"50000"},"sta":{"client_port":"50000","ap_port":"50500"},"ap":{"ip":"192.168.11.1","sta_port":"50000"}}' python config_mango_routes/config_routes.py
```

## NC
```
nc -u -l 50000
nc -u 10.30.1.1 50000
```

## IRTT
```
irtt server -b 0.0.0.0:50000
irtt client -i 100ms -d 10s -l 172 --fill=rand 10.30.1.1:50000 --local=0.0.0.0:50000
```
