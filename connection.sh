#!/bin/bash

#    Can supports up to 10 cars
#    if more, when searching for the last hotspot, it will consider that:
#        wifi_master_2 > wifi_master_10, it's because of getLastESSID()

# A raspi is always master of one, and the slave of another (thx to the 2 wifi cards)

#global variables:
INTERFACE0=wlan0
INTERFACE1=wlan1

#
#    Scan all the wifi networks
#    get only those starting with wifi_master_
#    Sort them
#    Get the last one
#
#    i.e:
#        wifi_master_0
#        wifi_master_1
#        wifi_master_2   <- will return this one
getLastESSID(){
    local res= iw dev $INTERFACE0 scan | egrep "SSID: wifi_master_" | sort -k 2 -g | tail -1
    echo res
}

#
#    Get the last wifi network starting with wifi_master_
#    add + 1 to the last number
#
#    i.e:
#        wifi_master_0 -> wifi_master_1
getNewESSID(){
    local essid=$(getLastESSID)
    local lastChar=${essid: -1}
    ((lastChar++))
    echo "wifi_master_"${lastChar}
}


#Master:
#    The raspi creates an ad-hoc network
#    Another raspi (slave) will have to connect to it (see: connect() )
createAdHocNetwork(){
    local essid=$(getNewESSID)

    echo "Creating ad-hoc network..."
    ifconfig $INTERFACE1 down
    iwconfig $INTERFACE1 mode ad-hoc
    iwconfig $INTERFACE1 essid $essid
    ifconfig $INTERFACE1 192.168.1.1 netmask 255.255.255.0 up
    echo "Ad-hoc network created"
}


#Slave:
#    The raspi connects to another raspi master wifi ad-hoc network.
connect(){
    local essid=$(getLastESSID)

    echo "Trying to connect to Master..."
    iwconfig $INTERFACE0 essid $essid
    ifdown $INTERFACE0
    ifconfig $INTERFACE0 192.168.1.2 netmask 255.255.255.0 up
    echo "Connected"
}


#if code executed in cars (no arg)
if [ "$#" -eq 0 ];then
    echo "================================="
    echo "Master Hotspot creation"
    echo "================================="
    createAdHocNetwork

    echo "================================="
    echo "Connection to Master"
    echo "================================="
    connect

# otherwise, $1 == computer's wifi interface
else
    echo "================================="
    echo "Computer Hotspot creation"
    echo "================================="

    echo "Creating ad-hoc network on interface: $1"
    ifconfig $1 down
    iwconfig $1 mode ad-hoc
    iwconfig $1 essid wifi_master_0
    ifconfig $1 192.168.1.1 netmask 255.255.255.0 up
    echo "Ad-hoc network created"

fi


exit 0


