import os
import paramiko
import json
import socket
import re
import time

WAIT_DURATION_SEC=40
POLLING_INTERVAL=10

# Example:
# DESIGN='mango' SDR='sdr-01' SIDE='sta' CONFIG='{"mac_addr":"40:d8:55:04:20:19"}' JSON_PATH='../sdrs.json' python start_mango.py
# DESIGN='mango' SDR='sdr-02' SIDE='ap' CONFIG='{"mac_addr":"40:d8:55:04:20:12"}' JSON_PATH='../sdrs.json' python start_mango.py

def check_host(server_ip,port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((server_ip, port))
        sock.close()
        if result == 0:
            return True
        else:
            return False

    except KeyboardInterrupt:
        print ("You pressed Ctrl+C")
        sys.exit()
    except socket.gaierror:
        return False
    except socket.error:
        return False

def parse_iwinfo(inp):

    lines = inp.splitlines()
    res_dict = {}
    for line in lines:
        if "," in line:
            if "(" in line and ")" in line:
                line = re.sub(r'\([^)]*\)', '', line)
            sections = line.split(',')
            sections = [ sec.strip() for sec in sections ]
            for sec in sections:
                sec.strip()
                if ":" in sec:
                    subsecs = sec.split(":")
                    subsecs = [ssec.strip() for ssec in subsecs]
                else:
                    subsecs = sec.split(" ")
                res_dict[subsecs[0]] = subsecs[1]
        else:
            res_dict[line.split(' ', 1)[0].replace('\t','')] = line.split(' ', 1)[1].replace('\t','')
    return res_dict


def run_cmd_mango(ip,command):

    username = "root"
    password = "root"
    print(f"SSHing to {ip}, username:{username}, password: {password}")

    # initialize the SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()

    # execute the command
    print(f"running command on {ip}: \n{command}")
    stdin, stdout, stderr = client.exec_command(command)
    stdout = stdout.read().decode().strip()
    if stdout:
        print(f"command stdout: \n{stdout}")
    stderr = stderr.read().decode().strip()
    if stderr:
        print(f"command sdterr: \n{stderr}")

    # close socket
    if client is not None:
        client.close()

    return stdout,stderr

def run_cmds_mango(ip,commands):

    # commands example
    # commands = [
    #     'cat file.txt',
    #     'cat file2.txt',
    # ]

    username = "root"
    password = "root"
    print(f"SSHing to {ip}, username:{username}, password: {password}")

    # initialize the SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()

    # execute the command
    for command in commands:
        print(f"running command on {ip}: \n{command}")
        stdin, stdout, stderr = client.exec_command(command)
        stdout = stdout.read().decode().strip()
        if stdout:
            print(f"command stdout: \n{stdout}")
        stderr = stderr.read().decode().strip()
        if stderr:
            print(f"command sdterr: \n{stderr}")

    # close socket
    if client is not None:
        client.close()

def check_mango(ip):

    status = {
        "wlan0_created": False,
        "wlan0_link": {},
        "wlan0_info": {},
        "wlan0_up": False,
        "wlan0_ip": ''
    }

    # check if wlan0 is created
    stdout, stderr = run_cmd_mango(
        ip,
        '/usr/sbin/ethtool wlan0 2>&1 | grep -q "Cannot get device settings: No such device" && echo "no" || echo "yes"',
    )
    status["wlan0_created"] = True if stdout == "yes" else False

    # check wlan0 properties if created
    if status["wlan0_created"]:
        stdout, stderr = run_cmd_mango(
            ip,
            '/usr/sbin/iw dev wlan0 info',
        )
        status["wlan0_info"] = parse_iwinfo(stdout)

    # check if wlan0 is up if created
    if status["wlan0_created"]:
        stdout, stderr = run_cmd_mango(
            ip,
            '/usr/sbin/ethtool wlan0 2>&1 | grep -q "Link detected: yes" && echo "yes" || echo "no"',
        )
        status["wlan0_up"] = True if stdout == "yes" else False

    # if wlan0 is up, read the ip
    if status["wlan0_up"]:
        stdout, stderr = run_cmd_mango(
            ip,
            "/sbin/ifconfig wlan0 | grep 'inet addr:' | cut -d: -f2| cut -d' ' -f1",
        )
        status["wlan0_ip"] = stdout

    return status


def check_sdr(sdr,json_path):
    with open(json_path) as json_file:
        sdrs_dict = json.load(json_file)

    result = {}
    for design in sdrs_dict[sdr]:
        result[design] = {}
        server_ip = sdrs_dict[sdr][design]['ip']
        port = int(sdrs_dict[sdr][design]['port'])
        result[design]['ip'] = server_ip
        result[design]['up'] = check_host(server_ip,port)

    return result


if __name__ == "__main__":

    sdr = os.environ['SDR']
    json_path = os.environ['JSON_PATH']
    side = os.environ['SIDE'].lower()
    wifi_conf = json.loads(os.environ['CONFIG'])

    print(f'You have chosen {sdr} as a {side} and wifi config: \n{wifi_conf}')
    sdr_status = check_sdr(sdr,json_path)
    if not sdr_status['mango']['up']:
        print(f"{sdr} is not a mango device")
        exit(0)

    mango_status = check_mango(sdr_status['mango']['ip'])
    sdr_status['mango'] = { **sdr_status['mango'] , **mango_status }
    print(f"{sdr} status:")
    print(json.dumps(sdr_status, indent = 4))

    if not sdr_status['mango']['wlan0_created']:

        # modeprobe mango_wlan
        stdout, stderr = run_cmd_mango(
            sdr_status['mango']['ip'],
            '/sbin/modprobe mango_wlan',
        )


        # delete iw device
        stdout, stderr = run_cmd_mango(
            sdr_status['mango']['ip'],
            '/usr/sbin/iw wlan0 del',
        )

        # create a new interface with the new mac_addr
        stdout, stderr = run_cmd_mango(
            sdr_status['mango']['ip'],
            f'/usr/sbin/iw phy mango-wlan-phy interface add wlan0 type managed addr {wifi_conf["mac_addr"]}',
        )

    else:
        print(f"{sdr} already has wlan0, it is advised to reboot it.")

    # ready to run the iw commands
    if side == 'sta':
        run_cmds_mango(
            sdr_status['mango']['ip'],
            [
                "/usr/sbin/wpa_supplicant -B -i wlan0 -d nl80211 -c /home/root/wpa_supplicant.conf",
                "/bin/sleep 10",
                "/sbin/udhcpc -i wlan0 -b",
            ]
        )


    elif side == 'ap':
        run_cmds_mango(
            sdr_status['mango']['ip'],
            [
                "/usr/bin/killall dnsmasq",
                "/usr/sbin/hostapd -B /home/root/hostapd.conf",
                "/bin/sleep 10",
                "/sbin/ifconfig wlan0 up 192.168.11.1 netmask 255.255.255.0",
                "/sbin/route add -net 192.168.11.0 netmask 255.255.255.0 gw 192.168.11.1",
                "/usr/bin/dnsmasq --interface=wlan0 --except-interface=lo --bind-interfaces --dhcp-range=192.168.11.2,192.168.11.30,255.255.255.0,12h --conf-file=/dev/null",
                "/usr/sbin/iptables --table nat --append POSTROUTING --out-interface eth0 -j MASQUERADE",
                "/bin/echo 1 > /proc/sys/net/ipv4/ip_forward",
            ]
        )

    # Wait for the new design
    success = False
    t_end = time.time() + WAIT_DURATION_SEC * 1
    print(f'Waiting {WAIT_DURATION_SEC} seconds for the new desgin to load')
    while time.time() < t_end:
        print(f"{POLLING_INTERVAL} seconds to the next poll...")
        time.sleep(POLLING_INTERVAL)
        check_dict = check_mango(sdr_status['mango']['ip'])
        if check_dict['wlan0_ip']:
            success = True
            break

    if success:
        print(f'{sdr} mango is running {side} with ip {check_dict["wlan0_ip"]}.')
    else:
        print(f'{sdr} mango start {side} did not work.')

