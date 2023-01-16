import os
import scan_test
import paramiko
import time
design = os.environ['DESIGN']
sdr_addr = os.environ['SDR']
#print(os.getenv("DESIGN"))
#print("Testing: %s" % design_mode)

#Uncomment and change according to your liking if you want to run the script alone
#design = 'ni'
#sdr_addr = 'sdr-02'

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

dict2 = scan_test.func1()
print("="*50, 'scanning', "="*50)
print(dict2)

#choosing IP address of the SDR and flavour
if sdr_addr == 'sdr-01' and design == 'ni':
    if dict2.get('sdr-01-ni.expeca')[3]=='Down' and dict2.get('sdr-01-mango.expeca')[3]=='Up':
        ip = dict2.get('sdr-01-mango.expeca')[1]
        ssh_connection(ip,design)
    elif dict2.get('sdr-01-ni.expeca')[3] == 'Up':
        print('ni already up')
    else:
        print('Both ni and mango are down')


if sdr_addr == 'sdr-01' and design == 'mango':
    if dict2.get('sdr-01-mango.expeca')[3]=='Down' and dict2.get('sdr-01-ni.expeca')[3]=='Up':
        ip = dict2.get('sdr-01-ni.expeca')[1]
        ssh_connection(ip,design)
    elif dict2.get('sdr-01-mango.expeca')[3] == 'Up':
        print('mango already up')
    else:
        print('Both ni and mango are down')


if sdr_addr == 'sdr-02' and design == 'ni':
    if dict2.get('sdr-02-ni.expeca')[3]=='Down' and dict2.get('sdr-02-mango.expeca')[3]=='Up':
        ip = dict2.get('sdr-02-mango.expeca')[1]
        ssh_connection(ip,design)
    elif dict2.get('sdr-02-ni.expeca')[3] == 'Up':
        print('ni already up')
    else:
        print('Both ni and mango are down')

if sdr_addr == 'sdr-02' and design == 'mango':
    if dict2.get('sdr-02-mango.expeca')[3]=='Down' and dict2.get('sdr-02-ni.expeca')[3]=='Up':
        ip = dict2.get('sdr-02-ni.expeca')[1]
        ssh_connection(ip,design)
    elif dict2.get('sdr-02-mango.expeca')[3] == 'Up':
        print('mango already up')
    else:
        print('Both ni and mango are down')



