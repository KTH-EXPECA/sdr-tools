#!/usr/bin/env python
# python scan.py

import socket
import subprocess
import sys
from datetime import datetime
import os
import re
def read_sdr_dict():
    # Define hosts to scan
    hosts = {
        'controller-01.expeca' : {
            'port' : 22
        },
        'mgmt-switch-01.expeca' : {
            'port' : 80
        },
        'tenant-switch-01.expeca' : {
            'port' : 22
        },
        'storage-01.expeca' : {
            'port' : 22
        },
        'worker-01.expeca' : {
            'port' : 22
        },
        'worker-02.expeca' : {
            'port' : 22
        },
        'worker-03.expeca' : {
            'port' : 22
        },
        'worker-04.expeca' : {
            'port' : 22
        },
        'worker-05.expeca' : {
            'port' : 22
        },
        'worker-06.expeca' : {
            'port' : 22
        },
        'poe-switch-01.expeca' : {
            'port' : 80
        },
        'poe-switch-02.expeca' : {
            'port' : 80
        },
        'sdr-01-ni.expeca' : {       
            'port' : 22              
        },                           
        'sdr-01-mango.expeca' : {     
            'port' : 22              
        },                           
        'sdr-02-ni.expeca' : {       
            'port' : 22              
        },                           
        'sdr-02-mango.expeca' : {     
            'port' : 22           
        },                        
    }                             
                                  
    # Print a nice banner with information on which host we are about to scan
    #print "-" * 90                                                           
    #print ("{:<30} {:<20} {:<10} {:<20}".format('HOST','IP','PORT','STATUS'))
    df = {} 
    dict2 = {}
    for host in hosts:                                                       
        remoteServer = host                                                  
        port = hosts[host]['port']                                           
                                                                             
        #print "-" * 90                                                       
                                                                             
        # We also put in some error handling for catching errors             
        try:                                                                 
            remoteServerIP  = socket.gethostbyname(remoteServer)             
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
            sock.settimeout(0.5)                                             
            result = sock.connect_ex((remoteServerIP, port))                 
            sock.close()                                                     
            if result == 0:                                                  
                resStr = 'Up'                                                
            else:                                                            
                resStr = 'Down'                                              
                                                                             
        except KeyboardInterrupt:                                            
            print ("You pressed Ctrl+C")                                       
            sys.exit()        
        except socket.gaierror:                                              
            remoteServerIP = '-'                                             
            resStr = 'Hostname not found'                                    
                                                                             
        except socket.error:                                                 
            print ("Couldn't connect to server")                               
            sys.exit()                                                       
        df.setdefault(host, []).extend([remoteServer,remoteServerIP,port,resStr])
        
       # print ("{:<30} {:<20} {:<10} {:<20}".format(remoteServer,remoteServerIP,port,resStr))
    #print(df)
    
    for key,value in df.items():
        if re.search('sdr', key):
            dict2.update({key:value})
    return dict2
   # print(state, ":", capital)
    #os.environ['lookup'] = df
    #print "-" * 90
