# :star: SNMP_NETSTAT_MIMIC

Programa que utiliza o SNMP para apresentar as portas em uso na rede dos protocolos UDP e TCP para o IP 127.0.0.1, por default, ou para um IP fornecido e que esteja com o SNMPD configurado.

## :sparkles: Execução

```
$ git clone https://github.com/paulacampigotto/snmp-netstat.git
$ cd snmp-netstat
$ python3 snmp-netstat.py
```

## :sparkles: Comandos do programa

```
#varreduraPortas                           // TCP e UDP do localhost
#varreduraPortas -TCP                      // TCP do localhost
#varreduraPortas -UDP                      // UDP do localhost
#varreduraPortas <endereco_ip>             // TCP e UDP do IP <endereco_ip>
#varreduraPortas <endereco_ip> -TCP        // TCP do ip <endereco_ip>
#varreduraPortas <endereco_ip> -UDP        // UDP do ip <endereco_ip>
help                                       // Comandos utilizáveis
exit                                       // Sair do programa
```

obs: não foi feito tratamento de erros, então digite os comandos conforme indicado :stuck_out_tongue_closed_eyes: 
