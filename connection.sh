#!/bin/bash

"""
    Can supports up to 10 cars
    if more, when searching for the last hotspot, it will consider that:
        wifi_master_2 > wifi_master_10, it's because of getLastESSID()

"""

#global variables:
INTERFACE0=wlan0
INTERFACE1=wlan1

getLastESSID(){
    local res= iw dev $INTERFACE0 scan | egrep "SSID: wifi_master_" | sort -k 2 -g | tail -1
    echo res
}

getNewESSID(){
    local essid=$(getLastESSID)
    local lastChar=${essid: -1}
    ((lastChar++))
    echo "wifi_master_"${lastChar}
}

# create adhoc network
createAdHocNetwork(){
    local essid=$(getNewESSID)

    echo "Creating ad-hoc network..."
    ifconfig $INTERFACE1 down
    iwconfig $INTERFACE1 mode ad-hoc
    iwconfig $INTERFACE1 essid $essid
    ifconfig $INTERFACE1 192.168.1.1 netmask 255.255.255.0 up
    echo "Ad-hoc network created"
}

# connect to wifi
connect(){
    local essid=$(getLastESSID)

    echo "Trying to connect to Master..."
    iwconfig $INTERFACE0 essid $essid
    ifdown $INTERFACE0
    ifconfig $INTERFACE0 192.168.1.2 netmask 255.255.255.0 up
    echo "Connected"
}

echo "================================="
echo "Master Hotspot creation"
echo "================================="
createAdHocNetwork

echo "================================="
echo "Connection to Master"
echo "================================="
connect




exit 0


