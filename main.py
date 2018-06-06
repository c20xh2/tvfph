from lib import pihole_object
from time import sleep
from sys import argv
import argparse

def main(webpassword, server_ip):
	pihole_obj = pihole_object.pihole_obj(webpassword, server_ip)
	while True:
		pihole_obj.update()
		pihole_obj.print_stats()
		sleep(1)


parser = argparse.ArgumentParser()

parser.add_argument('-w', '--webpassword', help="WEBPASSWORD (found via cat /etc/pihole/setupVars.conf)", default = None)
parser.add_argument('-i', '--ip', help="IP address of the Pi-Hole server", default = '127.0.0.1')

args = parser.parse_args()

webpassword = args.webpassword
server_ip = args.ip

if args.webpassword is None:
	with open('WebPassword.txt', 'r') as passfile:
		for line in passfile:
			if 'WEBPASSWORD' in line:
				webpassword = line.replace('WEBPASSWORD', '').replace("'", '').replace('=','').strip()

main(webpassword, server_ip)
