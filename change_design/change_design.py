import os
import paramiko
import time
import json
import socket

WAIT_DURATION_SEC = 200
POLLING_INTERVAL = 10

# Example:
# DESIGN='mango' SDR='sdr-01' JSON_PATH='sdrs.json' python change_design.py

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

def check_all_sdrs(json_path):

    with open(json_path) as json_file:
        sdrs_dict = json.load(json_file)

    for sdr in sdrs_dict:
        for design in sdrs_dict[sdr]:
            server_ip = sdrs_dict[sdr][design]['ip']
            port = int(sdrs_dict[sdr][design]['port'])
            sdrs_dict[sdr][design]['up'] = check_host(server_ip,port)
            if sdrs_dict[sdr][design]['up']:
                print(f"{sdr} is reachable: {sdrs_dict[sdr]}")

    return sdrs_dict


def change_design(sdr,ip,desired_design,json_path):
    
    username = "root"
    if desired_design == "mango":
        password = ""
        command = 'cp /uboot/mango_bootbin/BOOT.bin /uboot/ ; /sbin/reboot > /dev/null 2>&1 &'
    elif desired_design == "ni":
        password = "root"
        command = 'cp /media/card/ni_bootbin/boot.bin /media/card/ ; /sbin/reboot > /dev/null 2>&1 &'
    else:
        print("Changing to this desired design is not implemented")

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
    stdin, stdout,stderr = client.exec_command(command)
    print(f"command stdout: \n{stdout.read().decode()}")
    print(f"command sdterr: \n{stderr.read().decode()}")
    
    # close socket
    if client is not None:
        client.close()

    # Wait for the new design
    success = False
    t_end = time.time() + WAIT_DURATION_SEC * 1
    print(f'Waiting {WAIT_DURATION_SEC} seconds for the new desgin to load')
    while time.time() < t_end:
        print(f"{POLLING_INTERVAL} seconds to the next poll...")
        time.sleep(POLLING_INTERVAL)
        check_dict = check_sdr(sdr,json_path)
        if check_dict[desired_design]['up']:
            success = True
            break

    if success:
        print(sdr + ' design has been changed to ' + desired_design)
    else:
        print(sdr + ' design change did not work')

    return success

if __name__ == "__main__":

    desired_design = os.environ['DESIGN']
    sdr = os.environ['SDR']
    json_path = os.environ['JSON_PATH']

    print(f'You have chosen {sdr} and design {desired_design}')
    sdrs_dict = check_all_sdrs(json_path)
    
    sdr_is_alive = False
    for des in sdrs_dict[sdr]:
        sdr_is_alive = sdr_is_alive or sdrs_dict[sdr][des]['up']
        if sdrs_dict[sdr][des]['up']:
            current_design = des

    if desired_design not in sdrs_dict[sdr]:     
        print('The chosen design does not exist for this SDR')
    elif sdrs_dict[sdr][desired_design]['up']:
        print(f'{desired_design} on {sdr} is already set')
    elif not sdr_is_alive:
        print(f'No design on {sdr} is reachable.')
    else:
        change_design(
                sdr,
                sdrs_dict[sdr][current_design]['ip'],
                desired_design,
                json_path
            )

