#!/bin/env bash

iw dev wlan0 scan |
egrep "signal|SSID" |
sed -e "s/\tsignal: //" -e "s/\tSSID: //" |
awk '{ORS = (NR % 2 == 0)? "\n" : " "; print}


#create ad hoc network
iwconfig wlan0 mode Ad-hoc
iwconfig wlan0 essid MyWifi


ifconfig wlan0 192.168.1.1 netmask 255.255.255.0
ifconfig wlan0 192.168.1.2 netmask 255.255.255.0






