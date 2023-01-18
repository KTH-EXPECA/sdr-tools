import os
import sdr_scan_status
import paramiko
import time
#design = os.environ['DESIGN']
#sdr_addr = os.environ['SDR']
#print(os.getenv("DESIGN"))
#print("Testing: %s" % design_mode)

#Uncomment and change according to your liking if you want to run the script alone
design = 'ni'
sdr_addr = 'sdr-01'

print('You have chosen', sdr_addr , 'and design' , design)
def ssh_connection(ip,design):
    
    print(ip)
    username = "root"
    if design == "mango":
        password = ""
        commands = 'cp /uboot/mango_bootbin/BOOT.bin /uboot/ ; /sbin/reboot > /dev/null 2>&1 &'
    else:
        password = "root"
        commands = 'cp /media/card/ni_bootbin/boot.bin /media/card/ ; /sbin/reboot > /dev/null 2>&1 &'

    print('password:',password)
    print(commands)
    
        
    # initialize the SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username=username, password=password)
    except:
        print("[!] Cannot connect to the SSH Server")
        exit()


    #execute the commands
    stdin, stdout,stderr = client.exec_command(commands)
    print(stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print(err)
    if client is not None:
        client.close()
        del client, stdin, stdout, stderr
    t_end = time.time() + 60 * 1
    print('Scanning for 60 seconds')
    while time.time() < t_end:
        print("Waiting 20 seconds to poll")
        time.sleep(10)
        design_status_dict = sdr_scan_status.read_sdr_dict()
        status = design_status_dict[sdr_addr + '-' + design+'.expeca'][3]
        print(status)
        if status == 'Up':
            break
    print(sdr-addr + 'design has been changed to' + design)
dict2 = sdr_scan_status.read_sdr_dict()
print("="*50, 'scanning', "="*50)
print(dict2)

#choosing IP address of the SDR and flavour
if design == 'mango':
    if dict2.get(sdr_addr+"-mango.expeca")[3]=='Down' and dict2.get(sdr_addr+"-ni.expeca")[3]=='Up':
        ip = dict2.get(sdr_addr+"-ni.expeca")[1]
        ssh_connection(ip,design)
    elif dict2.get(sdr_addr+"-mango.expeca")[3]=='Up':
        print('mango already up')
    else:
        print('Both ni and mango are down for'+sdr_addr)

elif design == 'ni':
    if dict2.get(sdr_addr+"-ni.expeca")[3]=='Down' and dict2.get(sdr_addr+"-mango.expeca")[3]=='Up':
        ip = dict2.get(sdr_addr+"-mango.expeca")[1]
        ssh_connection(ip,design)
    elif dict2.get(sdr_addr+"-ni.expeca")[3]=='Up':
        print('ni already up')
    else:
        print('Both ni and mango are down for'+sdr_addr)
else:
    print('The chosen design does not exist in our setup')




