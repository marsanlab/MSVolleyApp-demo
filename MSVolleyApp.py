import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
#import plotly.express as px # interactive charts 
import plotly.graph_objects as go
#import matplotlib.pyplot as plt # plot figures
import json
from PIL import Image # import images

# configure the streamlit page
## st.set_page_config can only be called once per app, 
## and must be called as the first Streamlit command in the script
st.set_page_config(
    page_title = 'Volleyball Tracer',
    page_icon = '✅',
    layout = 'wide'
)


###########
# read player data from a json file
#@st.cache()
def load_player_data():
    with open('./player_data.json') as rjson:
        pdjson= json.load(rjson)
    return pd.DataFrame(pdjson)

player = load_player_data()

##########
def plot_selected_player_data(data):
    xright = go.Scatter(x = [8,8], y = [-2, 18], 
                         mode = 'lines', showlegend = False,
                         marker = dict(color = 'white', line = dict(width = 2)))
    ytop = go.Scatter(x = [0,8], y = [16, 16], 
                         mode = 'lines', showlegend = False,
                         marker = dict(color = 'white', line = dict(width = 2)))
    midline = go.Scatter(x = [0,8], y = [8, 8], 
                         mode = 'lines', showlegend = False,
                         marker = dict(color = 'black', line = dict(width = 2)))
    ydown = go.Scatter(x = [0,8], y = [0, 0], 
                         mode = 'lines', showlegend = False,
                         marker = dict(color = 'white', line = dict(width = 2)))

    mylayout = go.Layout(xaxis = dict(title = 'X location', zeroline = True,
                                  range = [-1,9], dtick =2, showgrid = False), 
                         yaxis = dict(title = 'Y location', zeroline = False,
                                  range = [-2, 18], dtick = 2, showgrid = False),
                         showlegend = False,
                         width=720, height=540)

    idname = data['id'][0].astype(str)
    trace = go.Scatter(x = data['xpos'],
                        y = data['ypos'],
                        mode = "markers",
                        name = idname,
                        marker = {'size': 5})
    fig = go.Figure(data = [xright, ytop, midline, ydown, trace], layout = mylayout)
    fig.add_annotation(x=data['xpos'][1], y=data['ypos'][1],
                       ax=data['xpos'][0], ay=data['ypos'][0],
                       xref='x', yref='y', axref='x', ayref='y',
                       showarrow=True, arrowhead=5, arrowsize=1.25, arrowwidth=1, arrowcolor='black',
                       opacity=0.5, text=' ', font=dict(color='black')) 

    return fig

##########

# dashboard title
st.title("Volleyball Tracer")

gamelist = [player.datetime[0],player.datetime[-1]]
st.sidebar.markdown("### 1. Select the match date")
selected_date = st.sidebar.selectbox(" ", gamelist)

# top-level filters 
## instread of top-level box, set a side bar box
st.sidebar.markdown("### 2. Select the player id")
player_filter = st.sidebar.selectbox(" ", pd.unique(player['id']))

# dataframe filter 
player = player[player['id']==player_filter]

# select time interval
st.sidebar.markdown("### 3. Select the time interval")
options = np.array(player['datetime']).tolist()
(start_time, end_time) = st.sidebar.select_slider(" ",
                                          options = options,
                                          value = ('2022-08-10 16:02:22', '2022-08-10 16:20:09',),
                                          )
# select data within the time interval
player.index = pd.to_datetime(player.datetime)
player = player[start_time:end_time]

# creating a single-element container.
## use single-element container to separate each element
## good for update/replace each element
placeholder = st.empty()
#image_place = st.empty()

for seconds in range(len(player)-1):
#for seconds in range(3):
#while True: 
    
     with placeholder.container():
    
        # video screenshoot
        st.markdown("### Video Screenshot")
        image = Image.open('./images/player_image'+f'{seconds:02d}'+'.png')
        fig2 = st.image(image, caption = "Marked by Martina"+f"{seconds}", width=640)
            
        # player movement    
        st.markdown("### Player Movement")
        fig = plot_selected_player_data(player[seconds:seconds+2])
        st.write(fig)

        # create data table
        st.markdown("### Detailed Data View")
        st.dataframe(player)
        time.sleep(1)
    #placeholder.empty()

