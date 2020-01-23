#!/usr/bin/env python

import subprocess
import argparse
import re

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")
    args = parser.parse_args()
    if not args.interface:
        parser.error("[-] Specify interface, use --help for more info")
    elif not args.new_mac:
        parser.error("[-] Specify MAC address, use --help for more info")
    return args

def change_mac(interface, new_mac):
    print("[+] Changing MAC Address for " + interface + " to " + new_mac)
    subprocess.call(["/sbin/ifconfig", interface, "down"])
    subprocess.call(["/sbin/ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["/sbin/ifconfig", interface, "up"])
    op = raw_input("Do you want to show the config for " + interface + " ? [y/n] > ")
    if op == 'y' or op == 'Y':    
        subprocess.call(["/sbin/ifconfig", interface])
    elif not (op != 'y' or op != 'Y') and (op != 'n' or op != 'N'):
        print("You must enter y [yes] or n [no]")

def get_mac(interface):
    ifconfig_output = subprocess.check_output(["/sbin/ifconfig", interface])
    search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_output)

    if search_result:
        return search_result.group(0)
    else:
        print("[-] Could not read MAC address")

args = get_arguments()
current_mac = get_mac (args.interface)
print("Current MAC = " + str(current_mac))
change_mac(args.interface, args.new_mac)

current_mac = get_mac (args.interface)
if current_mac == args.new_mac:
    print("[+] Succesfully changed MAC to " + current_mac)
else:
    print("[-] Error when changing MAC")


