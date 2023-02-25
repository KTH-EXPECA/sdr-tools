import os
import paramiko
from os import environ
import json
import socket
import re

# Example:
# SDR='sdr-02' SIDE='sta' JSON_PATH='../sdrs.json' OUTPUT_PATH='/home/wlab/irtt_data/wifi/info_pt2_low.json' SPEED_CHECK='192.168.11.1' python check_mango.py

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


def parse_iwlink(inp):

    lines = inp.splitlines()
    res_dict = {}
    for idx,line in enumerate(lines):
        if idx == 0:
            line = re.sub(r'\([^)]*\)', '', line)
            line = line.strip()
            sections = line.split(' ')
            res_dict['ap mac'] = sections[2].replace('\t','')
        else:
            if line.strip():
                sections = line.split(':')
                res_dict[
                    sections[0].replace('\t','')
                ] = sections[1].strip().replace('\t','')

    return res_dict

def parse_iwstationdump(inp):

    lines = inp.splitlines()
    res_dict = {}
    for idx,line in enumerate(lines):
        
        if line.split()[0] == "Station":
            line = re.sub(r'\([^)]*\)', '', line)
            line = line.strip()
            sections = line.split(' ')
            device = sections[1].replace('\t','')
            res_dict[device] = {}
        else:
            if line.strip():
                sections = line.split(':')
                res_dict[device][
                    sections[0].replace('\t','')
                ] = sections[1].strip().replace('\t','')

    return res_dict


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

    # check wlan0 link if it is STA and up
    if status["wlan0_up"] and status["wlan0_info"]["type"] == "managed":
        stdout, stderr = run_cmd_mango(
            ip,
            '/usr/sbin/iw dev wlan0 link',
        )
        status["wlan0_link"] = parse_iwlink(stdout)

    # check wlan0 stations if it is AP and up
    if status["wlan0_up"] and status["wlan0_info"]["type"].lower() == "ap":
        stdout, stderr = run_cmd_mango(
            ip,
            '/usr/sbin/iw dev wlan0 station dump',
        )
        status["wlan0_link"] = parse_iwstationdump(stdout)

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
    if environ.get('SPEED_CHECK') is not None:
        speed_check_apip = os.environ['SPEED_CHECK'].lower()
        speed_check = True

    print(f'You have chosen {sdr} as a {side} and speed check: \n{speed_check}')

    sdr_status = check_sdr(sdr,json_path)
    if not sdr_status['mango']['up']:
        print(f"{sdr} is not a mango device")
        exit(0)
    
    mango_status = check_mango(sdr_status['mango']['ip'])
    sdr_status['mango'] = { **sdr_status['mango'] , **mango_status }
    print(f"{sdr} status:")
    print(json.dumps(sdr_status, indent = 4))

    if speed_check:
        if not sdr_status['mango']['wlan0_created']:
            print(f"{sdr} mango no wlan0 was found.")
            exit(0)

        if not sdr_status['mango']['wlan0_up']:
            print(f"{sdr} mango wlan0 is not up")
            exit(0)

        if sdr_status['mango']['wlan0_info']['type'] == 'managed':
            if side == 'ap':
                print(f"{sdr} mango is STA not {side}.")
                exit(0)
        
        if sdr_status['mango']['wlan0_info']['type'].lower() == 'ap':
            if side == 'sta':
                print(f"{sdr} mango is AP not {side}.")
                exit(0)

        if speed_check and side=='ap':
            print(f"speed check should be run on STA side")
            exit(0)

        # ready to run the iperf commands
        stdout, strerr = run_cmd_mango(
            sdr_status['mango']['ip'],
            "/usr/bin/iperf3 -c {0} -u -bidir -b 1G -J --get-server-output".format(speed_check_apip)
        )
        sdr_status['mango']["wlan0_speed"] = json.loads(stdout)

    if environ.get('OUTPUT_PATH') is not None:
        output_path = os.environ['OUTPUT_PATH']
        with open(output_path, "w") as write_file:
            json.dump(sdr_status, write_file, indent=4)

