from lib import pihole_object
from time import sleep
from sys import argv


def get_line_numbers():
	z = 0
	line = None
	with open('WebPassword.txt', 'r') as passfile:
		for line in passfile:
			if '###' in line:
				pass
			else:
				line = line.replace('WEBPASSWORD', '').replace("'", '').replace('=','').strip()
				z+=1
	return z, line




def main(webpass):
	pihole_obj = pihole_object.pihole_obj(webpass.strip())
	while True:
		pihole_obj.update()
		pihole_obj.print_stats()
		sleep(1)


z, webpass = get_line_numbers()

if z != 1:
	if len(argv) != 2:
		print('\n\nError, please provide the WEBPASSWORD (found via cat /etc/pihole/setupVars.conf)\n')
	else:
		webpass = str(argv[1])
		main(webpass)

else:
	main(webpass)
