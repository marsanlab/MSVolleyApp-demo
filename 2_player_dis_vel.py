import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime
import json

## "apply" for DataFrame
## calculate distance and speed
def ds_speed(data):
    ## ds
    data['ds'] = round((data['dx']**2 + data['dy']**2)**0.5, ndigits=3)
    ## ds/dt
    data['speed']  = round(data['ds']/data['dt'], ndigits = 3)   
    return data

## convert timestring
def timestring(dstamp):
    time_struct = time.localtime(dstamp)
    timestring = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
    return timestring

### read json file to obtain player data
with open('./Volleyball/player_output.json') as rf:
    playerdata = json.load(rf)

## player's team, name, and other
time0 = playerdata['time_ref']
player_info = pd.DataFrame(playerdata['player_info'])
icount = playerdata['player_info']['id']

## calculate distance and speed
for ic, iv in icount.items():
    player = pd.DataFrame(playerdata[ic])
    ip = [iv for ix in range(len(player))]
    
    # create date_time_string
    player['datetime'] = player['time'] + time0
    player['datetime'] = player['datetime'].apply(timestring)

    # calculate delta time, xpos, ypos
    player['dt'] = player['time']-player['time'].shift(1)
    player['dx'] = player['xpos']-player['xpos'].shift(1)
    player['dy'] = player['ypos']-player['ypos'].shift(1)
    # calculate distance and speed
    player = player.apply(ds_speed, axis =1)

    # inser id column
    player.insert(0, column = 'id', value = ip)
    
    if iv == 0:
        player_data = player
    else:
        player_data = pd.concat([player_data, player], ignore_index = True)

player_data

## rearrange columns and convert datetime to Timestamp
cols = player_data.columns.tolist()
cols.insert(1,cols.pop(cols.index('datetime')))
player_data = player_data[cols]

## DataFrame to json output
js = player_data.to_json('./Volleyball/player_data.json',orient = 'columns')

### read json file to obtain player data
##with open('./Volleyball/player_data.json') as rjson:
##	df = json.load(rjson)
##pd.DataFrame(df)