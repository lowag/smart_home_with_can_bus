#an example units file, it can be much more longer  
from datetime import datetime
units={
    0x101:{
            "name":"living_room_center_ceiling",    
            "type":"output",
            "group":"light",
            "subgroup":"LED_DRGB",
            "ramp_on":100,
            "ramp_off":0,
            "scale":1,
            "location":"living_room",
            "normal_start_command":[0x02,0xFF,0xBE,0x6F,20,0,0,0],
            "normal_stop_command":[0x04,255,255,255,100,0,0,0],#here only the 1st and 5th byte matters
            "normal_working_time":20,
            "night_start_command":[0x02,50,50,50,20,0,0,0],
            "night_stop_command":[0x04,0,0,0,20,0,0,0],
            "night_working_time":20,
            "enabled":1,
            "status":0,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now(),
            "shutdown_time":datetime.now(),
            "stay_on":0
            },
    0x102:{
            "name":"living_room_center_floor",    
            "type":"output",
            "group":"light",
            "subgroup":"LED_DRGB",
            "ramp_on":100,
            "ramp_off":0,
            "scale":1,
            "location":"hallway",
            "normal_start_command":[0x02,0xFF,0xBE,0x6F,20,0,0,0],
            "normal_stop_command":[0x04,255,255,255,10,0,0,0],
            "normal_working_time":20,
            "night_start_command":[0x02,50,50,50,20,0,0,0],
            "night_stop_command":[0x04,0,0,0,20,0,0,0],
            "night_working_time":20,
            "enabled":1,
            "status":0,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now(),
            "shutdown_time":datetime.now(),
            "stay_on":0
            },
    0x124:{
            "name":"left corner_motion",    
            "type":"input",
            "group":"sensors",
            "subgroup":"motion",
            "location":"living_room",
            "normal_start_command":"start_light",
            "normal_start_argument":[0x123],
            "normal_stop_command":"stop_light",
            "normal_stop_argument":[0x123],
            "night_start_command":"start_light",
            "night_start_argument":[0x121],
            "night_stop_argument":"",
            "enabled":1,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now()
            },
    
    0x125:{
            "name":"left_corner_light_sensor",    
            "type":"input",
            "group":"sensors",
            "subgroup":"light",
            "location":"living_room",
            "value":0,
            "threshold":6,
            "normal_start_command":"check_light_level",
            "normal_start_argument":[0x125,0x121,0x122,0x123,0x101,0x141,0x142,0x161,0x162,0x181,0x182,0x183],
            "night_start_command":"check_light_level",
            "night_start_argument":[0x125,0x121,0x122,0x123,0x101,0x141,0x142,0x161,0x162,0x181,0x182,0x183],
            "enabled":1,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now()
            },
    
    0x144:{
            "name":"shutter1",    
            "type":"output",
            "group":"shutter",
            "subgroup":"",
            "ramp_on":0,
            "ramp_off":0,
            "location":"living_room",
            "normal_start_command":[0x02,30,0,0,0,0,0,0],
            "normal_stop_command":[0x04,30,0,0,0,0,0,0],
            "normal_working_time":30,
            "night_start_command":[0x02,30,0,0,0,0,0,0],
            "night_stop_command":[0x04,30,0,0,0,0,0,0],
            "night_working_time":30,
            "enabled":1,
            "status":0,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now(),
            "shutdown_time":datetime.now(),
            "stay_on":0
            },
     
    0x164:{
            "name":"socket1",    
            "type":"output",
            "group":"socket",
            "subgroup":"",
            "ramp_on":0,
            "ramp_off":0,
            "location":"living_room",
            "normal_start_command":[0x02,30,0,0,0,0,0,0],
            "normal_stop_command":[0x04,30,0,0,0,0,0,0],
            "normal_working_time":30,
            "night_start_command":[0x02,30,0,0,0,0,0,0],
            "night_stop_command":[0x04,30,0,0,0,0,0,0],
            "night_working_time":30,
            "enabled":1,
            "status":0,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now(),
            "shutdown_time":datetime.now(),
            "stay_on":0
            },
    0x165:{
            "name":'living_room_temp_hum_sensor",    
            "type":"input",
            "group":"sensors",
            "subgroup":"temp_hum",
            "location":"living_room",
            "value":0,
            "threshold":0,
            "normal_start_command":"empty_func",
            "normal_start_argument":"",
            "night_start_command":"empty_func",
            "night_start_argument":"",
            "enabled":1,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now()
            },
    
    0x199:{
            "name":"circulation_pump",    
            "type":"output",
            "group":"dig_output",
            "subgroup":"",
            "location":"kitchen",
            "normal_start_command":[0x02,0x02,0x02,35,45,80,0,0],
            "normal_stop_command":[0x04,0x04,0x00,35,45,80,0,0],
            "normal_working_time":40,
            "night_start_command":[0x02,0x02,0x02,35,45,40,0,0],
            "night_stop_command":[0x04,0x04,0x00,35,45,40,0,0],
            "night_working_time":40,
            "enabled":1,
            "status":0,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now(),
            "shutdown_time":datetime.now(),
            "stay_on":0
            },
    0x19A:{
            "name":"hot_water_temp",    
            "type":"input",
            "group":"sensors",
            "subgroup":"temp",
            "location":"bathroom",
            "value":0,
            "threshold":0,
            "normal_start_command":"empty_func",
            "normal_start_argument":"",
            "night_start_command":"empty_func",
            "night_start_argument":"",
            "enabled":1,
            "mode":"normal",
            "last_message_to":[0,0,0,0,0,0,0,0],
            "last_message_ack":False,
            "last_message_to_time":datetime.now(),
            "attempt_number":0,
            "last_message_from":[0,0,0,0,0,0,0,0],
            "last_message_from_time":datetime.now()
            }
}

