#!/usr/bin/env python

import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Target network to scan hosts")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Specify target network, use --help for more info")
    return args

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout = 1, verbose = False)[0]

    hosts_list = []
    for element in answered_list:
        hosts_dict = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        hosts_list.append(hosts_dict)
    return hosts_list

def print_result(result_list):
    print("IP\t\t\tMAC Address\n++++++++++++++++++++++++++++++++++++++++++++++")
    for host in result_list:
        print(host["ip"] + "\t\t" + host["mac"])
    print("++++++++++++++++++++++++++++++++++++++++++++++")

args = get_arguments()

scan_result = scan(args.target)
print_result(scan_result)
