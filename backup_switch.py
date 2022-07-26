import telnetlib
import re
import time
from netmiko import ConnectHandler


# backup_switch.py. ver 0.0.1
# Script by snowffox. snowffox@gmail.com
#
# Supported Switch is Extreme EXOS switch and Cisco IOS switch
# Supported protocol is telnet and ssh.
#
# but, Extreme EXOS ssh is not supported because some problems...
#
# switch info : ip, id, passwd, port, protocol, vendor(split by tab(\t) char)


def runSSH(switch, command):
    if switch[5]=='cisco':
        device='cisco_ios'
    elif switch[5]=='extreme':
        device='extreme'
    else:
        print("%s is not supported...\n" %(switch[5]))
        exit()

    ssh_con=ConnectHandler(device_type=device, ip=switch[0], username=switch[2], password=switch[3], port=switch[1])
    if device=='cisco_ios':
        ssh_con.enable()
    data=ssh_con.find_prompt()+'\n'
    data+=ssh_con.send_command(command, delay_factor=2)
    ssh_con.disconnect()
    return data
    
def runTELNET(switch, command):
    tn=telnetlib.Telnet(switch[0], switch[1], 20)
    #tn.set_debuglevel(1)
    prompt=getPrompt(switch[5])
    tn.read_until(prompt[0].encode('ascii'))
    tn.write(switch[2].encode('ascii')+b"\n")
    tn.read_until(prompt[1].encode("ascii"))
    tn.write(switch[3].encode('ascii')+b"\n")
    #tn.write("disable clipaging".encode('ascii')+b"\n")
    tn.write(command.encode('ascii')+b"\n")
    tn.write("exit".encode('ascii')+b"\n")
    data=tn.read_all().decode('ascii')
    tn.close()
    return data

def getPrompt(vendor):
    if vendor=='cisco':
        prompt=['Username: ','Password: ']
    elif vendor=='extreme':
        prompt=['login: ', 'password: ']
    return prompt


def decCOMMAND(switch):
    if switch[5]=='cisco' and switch[4]=='telnet':
        command="terminal length 0\r\nshow run"
    elif switch[5]=='cisco' and switch[4]=='ssh':
        command='show run'
    elif switch[5]=='extreme'and switch[4]=='telnet':
        command="disable clipaging\r\nshow config"
    elif switch[5]=='extreme' and switch[4]=='ssh':
        command='show config'
    else :
        print("%s switch is not support..." %(switch[5]))
        exit()
    return command

def saveCONFIG(switch, data):
    fname=switch[0]+".txt"
    f=open(fname, "w")
    f.write(data)
    f.close()


fname="switch.txt"
f=open(fname, 'r')
while True:
    l=f.readline().strip('\n')
    if not l:
        break
    switch=l.split('\t')
    print(switch)
    n=len(switch)
    if n !=6:
        print("switch information format is wrong...\n")
        print(switch)
        continue
    else:
        print("switch information is...")
        print(switch)
        command=decCOMMAND(switch)
        if switch[4]=='ssh':
            result=runSSH(switch, command)
        elif switch[4]=='telnet':
            result=runTELNET(switch, command)
        else:
            print(switch[4])
            print("Not supported...")
            result="Not supported..."
        
        saveCONFIG(switch, result)

