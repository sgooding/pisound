#!/bin/bash
sudo pip install .
sudo chmod 644 pisound.service
sudo cp pisound.service /lib/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pisound.service
sudo systemctl start pisound.service
