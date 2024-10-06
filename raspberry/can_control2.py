#!/usr/bin/python3
#CAN message for drgb LED strip:
#can_data[0]: order 2:on, 4: off, 6: sending the last order when a MC ask for it
#can_data[1]: red value 0-0xFF
#can_data[2]: green value 0-0xFF
#can_data[3]: blue value 0-0xFF
#can_data[4]: ramp on 1x sec, ramp off 10x sec 0-0xFF
#can_data[5]: light pattern
#

import paho.mqtt.client as mqtt
import json
import pytz
import can
import sys
import time as t
import threading
import os.path
from os import path
import os
from datetime import datetime, date, time, timedelta

from pyA20.gpio import gpio
from pyA20.gpio import port


import home_units
from home_units import *


locations={
"living_room":{
            "mode":"normal",
            "motion_sensors_disabled_by_user":False,
            "motion_sensors_disabled_by_light":False
        },
"hallway":{
            "mode":"normal",
            "motion_sensors_disabled_by_user":False,
            "motion_sensors_disabled_by_light":False
        },
"bathroom":{
            "mode":"normal",
            "motion_sensors_disabled_by_user":False,
            "motion_sensors_disabled_by_light":False
        },
"bedroom":{
            "mode":"normal",
            "motion_sensors_disabled_by_user":False,
            "motion_sensors_disabled_by_light":False
        }, 
"kitchen":{
            "mode":"normal",
            "motion_sensors_disabled_by_user":False,
            "motion_sensors_disabled_by_light":False
        } 
}
normal_mode_hour=6
normal_mode_minute=0
night_mode_hour=20
night_mode_minute=45
bathroom_hum_sensor_address=0x19C
#mqtt topic:
topic_name="house"
time_out=0.5

# create a bus instance
# many other interfaces are supported as well (see below)
bus = can.Bus(interface='socketcan',channel='can0',bitrate=125000,receive_own_messages=False)


def start_light(a):
    #print("start light...")
    #print(a)
    for x in range(len(a)):
        
        if units[a[x]]["stay_on"]==0 and units[a[x]]["enabled"]==1:
            sending_can_message(a[x],units[a[x]][units[a[x]]["mode"]+"_start_command"])
            units[a[x]]["shutdown_time"]=datetime.now()+timedelta(seconds = units[a[x]][units[a[x]]["mode"]+"_working_time"])
            units[a[x]]["status"]=1
            t.sleep(0.1)
def stop_light(a):
    #print("stop light...")
    #print (a[0])
    for x in range(len(a)):
        sending_can_message(a[x],units[a[x]][units[a[x]]["mode"]+"_stop_command"])
        units[a[x]]["status"]=0
        t.sleep(0.1)
def empty_func(a):
    1

def sending_can_message(address,candata):
    global units
    message = can.Message(arbitration_id=address, is_extended_id=False,data=candata)
    bus.send(message, timeout=1)
    #print("Can data has sent")
    if address in units and candata!=[0,0,0,0,0,0,0,0]:
        units[address]["last_message_to"]=candata
        units[address]["last_message_to_time"]=datetime.now()
        units[address]["last_message_ack"]=False
        units[address]["attempt_number"]=1
        
def receiving_messages():
    global units
    try:
        while True:        
            for msg in bus:
                #print(hex(msg.arbitration_id))
                if  msg.arbitration_id in units and len(msg.data)==8:
                    if msg.data[0]>0:
                        units[msg.arbitration_id]["last_message_from"]=msg.data
                        units[msg.arbitration_id]["last_message_from_time"]=datetime.now()
                    
                    if units[msg.arbitration_id]["type"]=="output" and msg.data[0]==6:
                        sending_can_message(msg.arbitration_id,units[msg.arbitration_id]["last_message_to"])
                    elif units[msg.arbitration_id]["type"]=="output" and msg.data[0]%2==1:
                        units[msg.arbitration_id]["last_message_ack"]=True
                        if msg.data[0]==3:
                            units[msg.arbitration_id]["status"]=1
                        elif msg.data[0]==5:
                            units[msg.arbitration_id]["status"]=0    
                        send_mqtt_msg(msg.arbitration_id,msg.data)
                    elif units[msg.arbitration_id]["type"]=="input" and units[msg.arbitration_id]["enabled"]==1 and msg.data[0]==1:
                        #print ("motion")
                        
                        #print (units[msg.arbitration_id]["mode"])
                        globals()[units[msg.arbitration_id][units[msg.arbitration_id]["mode"]+"_start_command"]](units[msg.arbitration_id][units[msg.arbitration_id]["mode"]+"_start_argument"])
                        if msg.arbitration_id==bathroom_hum_sensor_address:
                            check_hum_bathroom(msg.data[2])
                        send_mqtt_msg(msg.arbitration_id,msg.data)
                        units[msg.arbitration_id]["value"]=msg.data[1]
                       
                    
                        
    except Exception as Argument:
        f = open("/root/cancontrol_exceptions.log", "a")
        f.write(str(datetime.now())+"CAN receiving_messages: "+str(Argument)+" "+str(msg.arbitration_id)+" "+str(msg.data)+"\n")
        
        f.close() 
        
def change_mode(mode):
    global units
    try:
        for address in units:
            units[address]["mode"]=mode
        if mode=="night":
        #ventillation in bedroom on
            sending_can_message(0x217,[0x02,0,0,0,0,0,0,0])
        elif mode=="normal":
        #ventillation in bedroom off
            sending_can_message(0x217,[0x04,0,0,0,0,0,0,0])
            
    except Exception as Argument:
        f = open("/root/cancontrol_exceptions.log", "a")
        f.write(str(datetime.now())+"change mode: "+str(Argument)+"\n")
        f.close() 
        

        
def check_addresses():
    global units,normal_mode_hour,normal_mode_minute,night_mode_hour,night_mode_minute
    try:
        now=datetime.now()
        night_mode_start=now.replace(hour=night_mode_hour, minute=night_mode_minute, second=0, microsecond=0)
        normal_mode_start=now.replace(hour=normal_mode_hour, minute=normal_mode_minute, second=0, microsecond=0)
        if (now>=normal_mode_start and now>=night_mode_start) or (now<normal_mode_start and now<night_mode_start):
            #print("night")    
            change_mode("night")
            flipflop=True
        else:
            #print("normal")    
            change_mode("normal")
            flipflop=False
                
        while True:
            now=datetime.now()
            night_mode_start=now.replace(hour=night_mode_hour, minute=night_mode_minute, second=0, microsecond=0)
            normal_mode_start=now.replace(hour=normal_mode_hour, minute=normal_mode_minute, second=0, microsecond=0)
            if ((now>=normal_mode_start and now>=night_mode_start) or (now<normal_mode_start and now<night_mode_start)) and flipflop==False:
                #print("nigth")    
                change_mode("night")
                
                flipflop=True
            elif now>normal_mode_start and now<night_mode_start and flipflop==True:
                #print("normal")    
                change_mode("normal")
                
                flipflop=False
            for address in units:
                #print(address)
                #print(units[address]["group"])
                t.sleep(0.1) 
                if units[address]["type"]=="output":
                    if units[address]["last_message_ack"]==True and datetime.now()>units[address]["last_message_from_time"] + timedelta(seconds = 30):
                        sending_can_message(address,[0,0,0,0,0,0,0,0])
                    elif units[address]["group"]!="shutter" and units[address]["status"]==1 and datetime.now()>units[address]["shutdown_time"] and units[address]["stay_on"]==0:
                        sending_can_message(address,units[address][units[address]["mode"]+"_stop_command"])
                        units[address]["status"]=0
                    if units[address]["last_message_ack"]==False and datetime.now()>units[address]["last_message_from_time"] + timedelta(seconds = 1):
                        #print("address")
                        sending_can_message(address,units[address]["last_message_to"])
                        units[address]["attempt_number"]+=1
                elif units[address]["type"]=="input" and datetime.now()>units[address]["last_message_from_time"] + timedelta(seconds = 30):
                        sending_can_message(address,[0,0,0,0,0,0,0,0])        
            #print(units[0x125]["value"])
            t.sleep(0.1)        
    except Exception as Argument:
        f = open("/root/cancontrol_exceptions.log", "a")
        f.write(str(datetime.now())+"CAN check_addresses"+str(Argument)+"\n")
        f.write("\n")
        f.close() 
        
thread1 = threading.Thread(target=receiving_messages)
thread1.start()

thread2 = threading.Thread(target=check_addresses)
thread2.start()  


def send_mqtt_msg(address,msg):
    global units
    try:
        if units[address]["subgroup"]=="LED_DRGB":
           
            
            rhex="{:02x}".format(msg[1])
            if rhex=="0":
                rhex="00"
            ghex="{:02x}".format(msg[2])
            
            if ghex=="0":
                ghex="00"
            bhex="{:02x}".format(msg[3])
            
            if bhex=="0":
                bhex="00"    
            if msg[0]==3:
                status="1"
            else:
                status="0"
            client.publish(topic_name,'{"sender_id":"python_client","address":"'+str(address)+'","color":"#'+rhex+ghex+bhex+'","status":"'+status+'","mode":"'+units[address]["mode"]+'","enabled":"'+str(units[address]["enabled"])+'"}')
        elif units[address]["group"]=="shutter":
            if msg[0]==3:
                status="1"
            else:
                status="0"
            client.publish(topic_name,'{"address":"'+str(address)+'","status":"'+status+'"}')
        elif units[address]["subgroup"]=="temp":
            client.publish(topic_name,'{"address":"'+str(address)+'","temp":"'+str(msg[1])+'"}')
        elif units[address]["subgroup"]=="temp_hum":
            client.publish(topic_name,'{"address":"'+str(address)+'","temp":"'+str(msg[1])+'","hum":"'+str(msg[2])+'"}')
        elif units[address]["subgroup"]=="light":
            client.publish(topic_name,'{"address":"'+str(address)+'","light":"'+str(msg[1])+'"}')
        elif units[address]["subgroup"]=="dtemp":
            client.publish(topic_name,'{"address":"'+str(address)+'","temp1":"'+str(msg[1])+'","temp2":"'+str(msg[2])+'"}')
        elif units[address]["subgroup"]=="gas":
            gas=int.from_bytes(msg[1:4], "little")
            client.publish(topic_name,'{"address":"'+str(address)+'","gas":"'+str(gas)+'"}')
        
    except Exception as Argument:
        f = open("/root/cancontrol_exceptions.log", "a")
        f.write(str(datetime.now())+" CAN SENDMQTT: "+str(Argument)+"\n")
        f.close()
        
        
def check_light_level(a):
    global units
   
    if 1==1 and units[a[0]]["threshold"]+3<units[a[0]]["last_message_from"][1]:
        
        b=[]
        for x in range(len(a)):
            if x>0:#the first number is the sensor's address
                b.append(a[x])
                units[a[x]]["enabled"]=0
                stop_light(b)                       
    elif units[a[0]]["threshold"]>units[a[0]]["last_message_from"][1]:
        for x in range(len(a)):
            if x>0:#the first number is the sensor's address
                units[a[x]]["enabled"]=1

def check_hum_bathroom(value):
    global units
   
    if value>60:
    #bathroom ventillation
        units[0x218]["enabled"]=1
        
    elif value<59:
        units[0x218]["enabled"]=0
        stop_light([0x218])


def user_set_a_light(location):
    global units, locations
    at_least_one_light_on=False
    
    for address in units:
        if units[address]["location"]==location and units[address]["subgroup"]=="LED_DRGB" and units[address]["stay_on"]==1:
            at_least_one_light_on=True
            break
    locations[location]["motion_sensors_disabled_by_light"]=at_least_one_light_on
    motion_sensor_offon(location)
    
def motion_sensor_offon(location):  
    
    for address in units:
        if units[address]["location"]==location and units[address]["subgroup"]=="motion":
            if locations[location]["motion_sensors_disabled_by_light"]==False and locations[location]["motion_sensors_disabled_by_user"]==False :
                units[address]["enabled"]=1
                #print("sensor on")
            else:
                units[address]["enabled"]=0
                #print("sensor off")
            
def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker 
    print("Connected with result code {0}".format(str(rc)))  
  

def on_message(client, userdata, msg):  
    try:
        if msg.topic==topic_name:
            try:
                m = json.loads(msg.payload.decode())
            except ValueError:
                #print("bad json")
                return 0,
            #drgb led    
            if "address" in m.keys() and int(m["address"],0) in units and units[int(m["address"],0)]["subgroup"]=="LED_DRGB" and "color" in m.keys() and m["sender_id"]!="python_client" and "order" in m.keys():
            #if 1==1:
                
                units[int(m["address"],0)]["stay_on"]=int(m["order"])
                units[int(m["address"],0)]["status"]=int(m["order"])
                if int(m["order"])==1:
                    sending_can_message(int(m["address"],0),[0x02,round(int(m["color"][1:3],16)*units[int(m["address"],0)]["scale"]),round(int(m["color"][3:5],16)*units[int(m["address"],0)]["scale"]),round(int(m["color"][5:7],16)*units[int(m["address"],0)]["scale"]),units[int(m["address"],0)]["ramp_on"],0,0,0])
                    units[int(m["address"],0)]["status"]=1
                    units[int(m["address"],0)]["shutdown_time"]= datetime.now()+timedelta(hours = 4)
                    units[int(m["address"],0)]["stay_on"]=1
                    user_set_a_light(units[int(m["address"],0)]["location"])
                elif int(m["order"])==0:
                    sending_can_message(int(m["address"],0),[0x04,int(m["color"][1:3],16),int(m["color"][3:5],16),int(m["color"][5:7],16),units[int(m["address"],0)]["ramp_off"],0,0])
                    units[int(m["address"],0)]["shutdown_time"]= datetime.now()
                    units[int(m["address"],0)]["status"]=0
                    units[int(m["address"],0)]["stay_on"]=0
                    user_set_a_light(units[int(m["address"],0)]["location"])
            elif "address" in m.keys() and int(m["address"],0) in units and "working_time" in m.keys():#shutter
                
                if int(m["order"])==2:
                    sending_can_message(int(m["address"],0),[0x02,m["working_time"],0,0,0,0,0,0])
                    units[int(m["address"],0)]["status"]=1
                elif int(m["order"])==12:
                    sending_can_message(int(m["address"],0),[12,m["working_time"],0,0,0,0,0,0])
                    units[int(m["address"],0)]["status"]=0
                elif int(m["order"])==4:
                    sending_can_message(int(m["address"],0),[0x04,m["working_time"],0,0,0,0,0,0])
                    units[int(m["address"],0)]["status"]=0
            elif "data_query" in m.keys():#dataquery from a browser
                for address in units:
                    if units[address]["location"]==m["data_query"]:
                        if units[address]["type"]=="input":
                            sending_can_message(address,[0,0,0,0,0,0,0,0])
                            t.sleep(0.1)
                        send_mqtt_msg(address,units[address]["last_message_from"])
                        #print(address)
                        t.sleep(0.1)
            elif "req_mode" in m.keys() and (m["req_mode"]=="normal" or m["req_mode"]=="night"):
                units[int(m["address"],0)]["mode"]=m["req_mode"];
                
            elif "location" in m.keys() and "motion_sensor" in m.keys() and m["motion_sensor"]=="1":
                locations[m["location"]]["motion_sensors_disabled_by_user"]=True
                
                motion_sensor_offon(m["location"])
            elif "location" in m.keys() and "motion_sensor" in m.keys() and m["motion_sensor"]=="0":
                locations[m["location"]]["motion_sensors_disabled_by_user"]=False
                motion_sensor_offon(m["location"])
    except Exception as Argument:
        f = open("/root/cancontrol_exceptions.log", "a")
        if "address" in m.keys():
            f.write(str(datetime.now())+" on_message mqqt: "+str(Argument)+m["address"]+"\n")
        else:
            f.write(str(datetime.now())+" on_message mqqt without address\n")
        f.close()

#change_mode("night")
#client.publish("company/"+loc+"/machines/"+machines,mes)
client = mqtt.Client("python_client")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect('127.0.0.1', 2883)
client.subscribe(topic_name)
client.loop_forever()
# Start networking daemon

