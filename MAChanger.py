#!/usr/bin/env python

import subprocess
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_argument("-m", "--mac", dest="new_mac", help="New MAC address")

args = parser.parse_args()

interface = args.interface
new_mac = args.new_mac

print("[+] Changing MAC Address for " + interface + " to " + new_mac)

subprocess.call(["/sbin/ifconfig", interface, "down"])
subprocess.call(["/sbin/ifconfig", interface, "hw", "ether", new_mac])
subprocess.call(["/sbin/ifconfig", interface, "up"])
op = raw_input("Do you want to show the new config for " + interface + " ? [y/n] > ")
if op == 'y' or op == 'Y':    
    subprocess.call(["/sbin/ifconfig", interface])
elif op == 'n' or op == 'N':
    print("[+] Done")
else:
    print("Error")