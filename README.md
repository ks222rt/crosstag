Crosstag: A sensible gym solution for sensible gyms
=========================
I really wish I had written more here. Maybe by Christmas?

Features
----------

- Designed to run on a Raspberry Pi (http://www.raspberrypi.org/products/)
- COTS RFID-reader compatible (https://www.sparkfun.com/products/retired/9875, https://www.sparkfun.com/products/13198)
- Stand alone server
- Stand alone reader
- Stand alone viewer
- Not much more

Installation
------------
### install dependencies and clone this repo
```sh
sudo pip3 install —upgrade pip
sudo pip3 install Flask
sudo pip3 install Flask-SQLAlchemy
sudo pip3 install Flask-wtf
sudo pip3 install pyfiglet
sudo pip3 install requests
sudo pip3 install pyserial
git clone https://github.com/lundstrj/crosstag.git
```
### to start the server
```sh
sudo python crosstag_server.py
```
### to start the reader
```sh
python crosstag_reader.py
```
### to start the terminal based viewer
```sh
python crosstag_viewer.py
```

Avoid screen blanking
---------------------
```sh
sudo nano /etc/kbd/config
```
```
BLANK_TIME=0
POWERDOWN_TIME=0
```
```sh
sudo /etc/init.d/kbd restart
sudo nano /etc/lightdm/lightdm.conf
xserver-command=X -s 0 dpms
```
Setup for remote access
-----------------------
```sh
sudo apt-get update
sudo apt-get install weavedconnectd
sudo weavedinstaller
```

Setup for Crontab
-----------------------
```sh
sudo apt-get install gnome-schedule
crontab -e <== Opens crontab file
Add 2 lines in the bottom for automatic email and automatic sync
* 10 * * 1 wget -O - -q -t 1 http://localhost/crosstag/v1.0/send_latecomers_emal
* 6 * * 1 wget -O - -q -t 1 http://localhost/crosstag/v1.0/fortnox
0 0 1 * * wget -O - -q -t 1 http://localhost/crosstag/v1.0/clear_tagcounter
```
