# tvfph
(terminal viewer for pi-hole)
This is a third party application, and may not always work with the latest version of Pi-hole
Pihole API Terminal Parsing

This script will show live stats from the Pi-Hole in a terminal.
Hostname resolution will work if the Pi-Hole is used as DHCP server.

![alt text](https://i.imgur.com/v828Ak1.png)

Requirements:
```pip3 install requests ```
```
usage: main.py [-h] [-w WEBPASSWORD] [-i IP]

optional arguments:
  -h, --help            show this help message and exit
  -w WEBPASSWORD, --webpassword WEBPASSWORD
                        WEBPASSWORD (found via cat /etc/pihole/setupVars.conf)
  -i IP, --ip IP        IP address of the Pi-Hole server
```

(You can also provide the WEBPASSWORD in WebPassword.txt)
    
