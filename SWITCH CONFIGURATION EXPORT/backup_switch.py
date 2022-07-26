import telnetlib
import re
import time
import paramiko
import concurrent.futures
import sys

# backup_switch.py. ver 0.0.5
# Script by snowffox.
#
# Document: https://blog.boxcorea.com/wp/archives/2277
#
# Supported Switch is Extreme EXOS switch and Cisco IOS switch
# Supported protocol is telnet and ssh.
#
#
# switch info : ip, port, user_id, passwd, protocol, vendor(split by tab(\t) char)
#
# ver 0.0.2 : Error handling. Support SSH with netmiko
# ver 0.0.3 : Full support SSH with paramiko and hostname support.
# ver 0.0.4 : Improve performance by using Thread.
# ver 0.0.5 : Support custom file name on command line option.



def runSSH(switch, command):
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=switch[0], port=switch[1], username=switch[2], password=switch[3])
        stdin, stdout, stderr=ssh.exec_command(command.encode('ascii'))
        data=((stdout.read()).decode('ascii')).replace('\r\n', '\n')
    except:
        print("ERROR 001: SSH Connection error...")
        data="error"
    return data
    
def runTELNET(switch, command):
    try:
        tn=telnetlib.Telnet(switch[0], switch[1], 20)
        #tn.set_debuglevel(1)
        prompt=getPrompt(switch[5])
        tn.read_until(prompt[0].encode('ascii'))
        tn.write(switch[2].encode('ascii')+b"\n")
        tn.read_until(prompt[1].encode("ascii"))
        tn.write(switch[3].encode('ascii')+b"\n")
        tn.write(command.encode('ascii')+b"\n")
        tn.write("exit".encode('ascii')+b"\n")
        data=tn.read_all().decode('ascii')
        tn.close()
    except:
        print("ERROR 002: TELNET Connection error...\n")
        data="error"


    return data

def getPrompt(vendor):
    if vendor=='cisco':
        prompt=['Username: ','Password: ']
    elif vendor=='extreme':
        prompt=['login: ', 'password: ']
    elif vendor=='nexus':
        prompt=['login: ','Password: ']
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
    elif switch[5]=='nexus' and switch[4]=='telnet':
        command="terminal length 0\r\nshow run"
    elif switch[5]=='nexus' and switch[4]=='ssh':
        command='show run'
    else :
        print("%s switch is not support..." %(switch[5]))
        command="not supported"
    return command


def gethostNAME(vendors, s):
    if s=="error":
        return "error"
    l=[]
    h=""
    if not s:
        s="ERROR 003 can not extract hosname!!!"
    if str.lower(vendors)=="cisco":
        pattern="hostname"
        dli=" "
    elif str.lower(vendors)=="extreme":
        pattern="configure snmp sysName"
        dli="\""
    else:
        print("ERR 004 vendors %s Hostname not support!" %(vendors))
        hostname=vendors
        return hostname

    l=(s.strip()).split('\n')
    for i in l:
        p=re.compile(pattern)
        m=p.match(i)
        if m :
            h=i

    l=h.split(dli)
    hostname=l[1].strip()
    return hostname

def saveCONFIG(switch, data):
    host=gethostNAME(switch[5], data)
    fname=host+'_'+switch[0]+".txt"
    f=open(fname, "w")
    f.write(data)
    f.close()

def main(switch):
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

    
if __name__=="__main__":
    argn=len(sys.argv)
    if argn==1:
        print("use default switch info file 'switch.txt'...")
        fname="switch.txt"
    elif argn>2:
        print("use only one switch info file\nProgram ended...")
        exit()
    else:
        fname=sys.argv[1]
        
    try:
        f=open(fname, 'r')
    except:
        print("File '%s' not found" %(fname))
        exit()
        
    while True:
        l=f.readline().strip('\n')
        if not l:
            break
        switch=l.split('\t')
    #   print(switch)
        n=len(switch)
        if n !=6:
            print("switch information format is wrong...\n")
            print(switch)
            continue
        else:
            pool=concurrent.futures.ProcessPoolExecutor(4)
            future=pool.submit(main, (switch))
            future.done()

    f.close()

