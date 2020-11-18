Raspberry Pi Setup Notes
===

Wiring
---

![RPi Wiring](img/led_strips_raspi_NeoPixel_powered_bb.jpg)

(from Adafruit's guide ["NeoPixels on Raspberyy Pi"](https://learn.adafruit.com/neopixels-on-raspberry-pi/raspberry-pi-wiring))

Install Neopixel Python Library
---

```
sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```

(from Adafruit's guide ["NeoPixels on Raspberyy Pi"](https://learn.adafruit.com/neopixels-on-raspberry-pi/python-usage))

Execute Script at Startup
---

Edit the `/etc/rc.local` file to look like:

```
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.

# Print the IP address
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
fi

## THIS SCRIPT WILL RUN AT STARTUP
##
/share/display-time-wheel_1.py 2>&1 >> /tmp/display.log &

exit 0
```

Samba Access
---

To allow for ease of accessibility, a Samba server was setup.

To install:

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install samba samba-common-bin
sudo mkdir -m 1777 /share
```

Add the following to `/etc/samba/smb.conf`:

```
[share]
Comment = Pi shared folder
Path = /share
Browseable = yes
Writeable = Yes
only guest = no
create mask = 0777
directory mask = 0777
Public = yes
Guest ok = yes
```

Add a password:

```
sudo smbpasswd -a pi
```

Restart Samba:

```
sudo /etc/init.d/samba restart
```

(following MagPi's ["Samba File Server"](https://magpi.raspberrypi.org/articles/samba-file-server) article).


