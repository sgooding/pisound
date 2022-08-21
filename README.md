# Pi Sound Board
A simple key sound board.

# Setup

## apt dependencies
sudo apt install python3-pygame python3-gpiozero python3-pydub

## samba
1. sudo apt install samba samba-common-bin
2. mkdir /home/pi/media
3. chmod -R a+rwX /home/pi/media
4. edit /etc/samba/smb.conf add to the bottom
```
[media]
path = /home/pi/media
writeable=Yes
create mask=0777
directory mask=0777
public=yes
```
5. sudo service restart smbd

Ref: https://pimylifeup.com/raspberry-pi-samba/


# Config

# Env

MEDIA_PATH=/home/pi/media


# Add as service
1. create service file /lib/systemd/system/pisound.service
```
[Unit]
Description=Pi Sound Board
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python -m pisound
Restart=on-abort

[Install]
WantedBy=multi-user.target
```
2. enable the service
```
sudo chmod 644 /lib/systemd/system/pisound.service
sudo systemctl daemon-reload
sudo systemctl enable pisound.service
sudo systemctl start pisound.service
```
3. status
```
Check status
sudo systemctl status pisound.service

Start service
sudo systemctl start pisound.service

Stop service
sudo systemctl stop pisound.service

Check service's log
sudo journalctl -f -u pisound.service
```

ref: https://gist.github.com/emxsys/a507f3cad928e66f6410e7ac28e2990f

# USB Audio Device
To use a USB audio device, you need to blacklist the default audio device.

1. Disable onboard audio.
```
Open /etc/modprobe.d/raspi-blacklist.conf and add blacklist snd_bcm2835.
```
2. Allow the USB audio device to be the default device.
```
Open /lib/modprobe.d/aliases.conf and comment out the line options snd-usb-audio index=-2
```
3. Reboot
```
sudo reboot
```
4. Test it out.
```
$ aplay /usr/share/sounds/alsa/Front_Center.wav
```

ref: https://superuser.com/questions/989385/how-to-make-raspberry-pi-use-an-external-usb-sound-card-as-a-default