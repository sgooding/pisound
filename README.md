# Pi Sound Board
A simple key sound board.

# Usage
Sound Board Features

## Power Off
Hold down any button for 5 seconds. 

## Power On after soft shutdown
Push button 2 or GPIO3 on pin 5.

## USB Stick Sound Upload
1. Power off raspberry pi.
2. Add exactly 4 songs to any USB key. .mp3 files only!
Files should look like this on the USB Key:
```
F:\any_song.mp3
F:\any_song2.mp3
F:\any_song3.mp3
F:\any_song4.mp3
```
3. Insert USB Stick into raspberry pi USB slot.
4. Power on the raspberry pi.
5. Wait for boot sound to play. Elevator music will play if any new files need conversion.

# Installation
```
# 1. Download the Code.
git clone https://github.com/sgooding/pisound.git
# 2. Install dependencies
sudo apt-get update; sudo apt-get install -y libsdl-dev
# 3. Install pisound
cd pisound
./scripts/install.sh
# Sound should be playing at this point.
```

# Setup

## Buttons
![Alt text](img/pi_board.png?raw=true "Raspberry Pi Pinout")

|Button|IO Pin|Pin|
|--------|--------|--|
|Button 1|GPIO2 | 3|
|Button 2|GPIO3 | 5|
|Button 3|GPIO4 | 7|
|Button 4|GPIO17| 11|
|Ground  |GND | 39 |


## apt dependencies
sudo apt install python3-pygame python3-gpiozero python3-pydub libsdl-dev

## samba
Warning: this slows boot when remote.
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
