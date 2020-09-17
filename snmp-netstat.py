import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    PURPLE = '\033[95m'
    DARKCYAN = '\033[36m'

DEFAULT_IP = '127.0.0.1'
DEFAULT_PROTOCOLS = ['TCP', 'UDP']
TCP_OID = '.1.3.6.1.2.1.6.13'
UDP_OID = '.1.3.6.1.2.1.7.7'

def printHelpMenu():
    print()
    print(bcolors.BOLD + '\t      Comando \t\t\t          Ação\n'+bcolors.ENDC)
    print('#varreduraPortas \t\t\t UDP e TCP do IP 127.0.0.1')
    print('#varreduraPortas -TCP \t\t\t TCP do IP 127.0.0.1')
    print('#varreduraPortas -UDP \t\t\t UDP do IP 127.0.0.1')
    print('#varreduraPortas <endereco_ip> \t\t UDP e TCP do IP <endereco_ip>')
    print('#varreduraPortas <endereco_ip> \t\t UDP e TCP do IP <endereco_ip>')
    print('#varreduraPortas <endereco_ip> -TCP \t TCP do IP <endereco_ip>')
    print('#varreduraPortas <endereco_ip> -UDP \t UDP do IP <endereco_ip>')
    print('exit \t\t\t\t\t Sair do programa')
    print('help \t\t\t\t\t Comandos utilizáveis\n')

    readInput()

def readInput():
    args = input(bcolors.OKGREEN+'~ '+bcolors.ENDC).split(' ')
    if(args[0] == 'exit'):
        quit()
    if(args[0] == 'help'):
        printHelpMenu()
    if len(args) == 1 or args[1]=='':
        return DEFAULT_IP, DEFAULT_PROTOCOLS
    if len(args) == 2 or args[2]=='':
        if '-' in args[1]:
            return DEFAULT_IP, [args[1].split('-')[1]]
        return args[1], DEFAULT_PROTOCOLS
    if len(args) == 3 or args[3] == '':
        return args[1], [args[2].split('-')[1]]

def cleanFiles():
    open('tcp.txt', 'w+').close()
    open('udp.txt', 'w+').close()

def request(ip, protocols):
    cleanFiles()
    for i in protocols:
        request = 'snmpwalk -v2c -c public ' + ip + ' '
        if i == 'UDP' or i == 'udp':
            request+= UDP_OID + ' >> udp.txt'
            os.system(request)
        elif i == 'TCP' or i == 'tcp':
            request+=TCP_OID + ' >> tcp.txt'
            os.system(request)
        else:
            print(bcolors.FAIL + "-> Protocolo inválido" + bcolors.ENDC)

def udpParser():
    localIpUdp = [] 
    localPortUdp = [] 
    remoteIpUdp = []
    remotePortUdp = []

    with open('udp.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if(line.startswith('UDP-MIB::udpEndpointProcess.ipv4."')):
            newLine = line.split('UDP-MIB::udpEndpointProcess.ipv4."')[1]
            localIpUdp.append(newLine.split('.')[0] + '.' + newLine.split('.')[1] + '.' + newLine.split('.')[2] + '.' + newLine.split('.')[3][:-1])
            localPortUdp.append(newLine.split('.')[4])
            newLine = line.split('."')[2]
            remoteIpUdp.append(newLine.split('.')[0] + '.' + newLine.split('.')[1] + '.' + newLine.split('.')[2] + '.' + newLine.split('.')[3][:-1])
            newLine = line.split('".')[2]
            remotePortUdp.append(newLine.split('.')[0])
    

    return localIpUdp, localPortUdp, remoteIpUdp, remotePortUdp

def tcpParser():
    localIpTcp = [] 
    localPortTcp = [] 
    remoteIpTcp = []
    remotePortTcp = []

    with open('tcp.txt', 'r') as file:
        lines = file.readlines()

    for line in lines:
        if(line.startswith('TCP-MIB::tcpConnState.') and line[-15:] == 'established(5)\n'):
            newLine = line.split('TCP-MIB::tcpConnState.')[1]
            splittedLine = newLine.split('.')
            localIpTcp.append(splittedLine[0] + '.' + splittedLine[1] + '.' + splittedLine[2] + '.' + splittedLine[3])
            localPortTcp.append(splittedLine[4])
            remoteIpTcp.append(splittedLine[5] + '.' + splittedLine[6] + '.' + splittedLine[7] + '.' + splittedLine[8])
            remotePortTcp.append(splittedLine[9].split(' ')[0])

    return localIpTcp, localPortTcp, remoteIpTcp, remotePortTcp




def printResults(protocols):
    localIpUdp, localPortUdp, remoteIpUdp, remotePortUdp = udpParser()
    localIpTcp, localPortTcp, remoteIpTcp, remotePortTcp = tcpParser()

    head = "  IP Local\t     Porta Local\t  IP remoto\t   Porta remota\n"
    fmt = "{b1:s}\t\t{b2:s}\t\t{b3:s}\t\t{b4:s}"

    for i in protocols:
        if(i == 'TCP' or i == 'tcp'):
            print(bcolors.HEADER + "\n---------------------------------- TCP ---------------------------------\n"+ bcolors.ENDC)
            print(bcolors.BOLD + head + bcolors.ENDC) 
            for item in range(len(localIpTcp)):
                print(fmt.format(b1=localIpTcp[item], b2=localPortTcp[item], b3=remoteIpTcp[item], b4=remotePortTcp[item]))
        if(i == 'UDP' or i == 'udp'):
            print(bcolors.HEADER + "\n\n\n---------------------------------- UDP ----------------------------------\n"+ bcolors.ENDC)
            print(bcolors.BOLD + head + bcolors.ENDC) 
            for item in range(len(localIpUdp)):
                if(remotePortUdp[item] != '0'):
                    print(fmt.format(b1=localIpUdp[item], b2=localPortUdp[item], b3=remoteIpUdp[item], b4=remotePortUdp[item]))
            print('\n')



def main():


    print(bcolors.HEADER + "\n -------------------------- SNMP_NETSTAT_MIMIC --------------------------\n\n"+bcolors.ENDC)

    while True:

        ip, protocols = readInput()

        request(ip,protocols)

        printResults(protocols)

if __name__ == "__main__":
    main()
