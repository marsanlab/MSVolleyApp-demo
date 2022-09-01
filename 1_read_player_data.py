import pandas as pd
import time
import datetime
import json


df = pd.read_csv('./testdata01.csv')
player_data={}

## convert str to timestamp
def datetime_stamp(tx):
    tstamp = int(time.mktime(time.strptime(tx, '%a %b %d %H:%M:%S %Y')))
    return tstamp

## return the xy_location
def xylocation(loc):
    xloc = loc.find('x')
    yloc = loc.find('y')
    xloc_start = loc.find('[')
    xloc_end = loc.find(']')
    yloc_start = loc[yloc:].find('[')
    yloc_end = loc[yloc:].find(']')

    xpos = loc[xloc_start+1:xloc_end]
    xpos =list(map(int, xpos.split(', ')))
    ypos = loc[yloc+yloc_start+1:yloc+yloc_end]
    ypos =list(map(int, ypos.split(', ')))

    return xpos, ypos

## extract player information
playerinfo = pd.DataFrame({'id':range(len(df))})
playerinfo[['team','name']] = df['player_name'].str.split('_', expand =True)
player_data={'player_info': playerinfo.to_dict() }

## create player movement data
for ic in range(len(df)):

    # calculate time step
    date = df.Time[ic].replace('[','').replace(']','').split(',')
    date = list(map(lambda x: x.strip(), date))
    date = list(map(lambda x: x[1:-1], date))
    timestamp = list(map(lambda x: datetime_stamp(x),date))
    
    if ic == 0:
        date0 = date[0]    
        time0 = timestamp[0]
        player_data['date_ref'] = date0
        player_data['time_ref'] = time0
        
    ptime = list(map(lambda x: x - time0, timestamp))

    # calculate player location
    xyloc = df.loc[ic,'Coordinates']
    
    xpos, ypos = xylocation(xyloc)
  
    player_data[ic] = {
              'time': ptime, 
              'xpos': xpos, 
              'ypos': ypos
             }

## convert python data into json and save as a json file -> json.dump()
## dump() uses json.JSONEncoder() convert files
with open('./player_output.json','w') as f:
    json.dump(player_data, f)


### read json file to obtain player data
##with open('./player_output.json') as rf:
##    playerdata = json.load(rf)