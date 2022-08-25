import streamlit as st # web development
import numpy as np # np mean, np random 
import pandas as pd # read csv, df manipulation
import time # to simulate a real time data, time loop 
import plotly.express as px # interactive charts 
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


# read player data from a json file
#@st.cache()
def load_player_data():
    with open('./player_data.json') as rjson:
        pdjson= json.load(rjson)
    return pd.DataFrame(pdjson)

player = load_player_data()

##########

# dashboard title

st.title("Volleyball Tracer App")

# top-level filters 
## instread of top-level box, set a side bar box
#job_filter = st.sidebar.selectbox("Select the Job", pd.unique(df['job']))
st.markdown("### Select the player id")
player_filter = st.selectbox("please select the player id", pd.unique(player['id']))

# creating a single-element container.
## use single-element container to separate each element
## good for update/replace each element
placeholder = st.empty()

# dataframe filter 
player = player[player['id']==player_filter]


# select time interval
st.markdown("### Select the time interval")
options = np.array(player['datetime']).tolist()
(start_time, end_time) = st.select_slider("please select the time interval",
                                          options = options,
                                          value = ('2022-08-10 16:02:22', '2022-08-10 16:20:09',),
                                          )
st.write("start_time: ", start_time, "  ~  end_time: ", end_time)


# select data in the time interval
#player['datetime'] = pd.to_datetime(player.datetime)
player.index = pd.to_datetime(player.datetime)

player = player[start_time:end_time]
# near real-time / live feed simulation 
# use random number to simulate real-time effect for 200 seconds

# progress bar
latest_iteration = st.empty()
bar = st.progress(0)

#image_place = st.empty()

for seconds in range(len(player)-1):
#while True: 
    
    latest_iteration.text(f"#{seconds+1}")
    bar.progress(seconds+1)

    # creating KPIs 

    selected_time = player['datetime'][seconds+1] 
    #delta_time = player['time'][seconds+1]-player['time'][seconds] 

    player_distance = player['ds'][seconds+1]
    delta_ds = player['ds'][seconds+1]-player['ds'][seconds]
    
    player_speed = player['speed'][seconds+1]
    delta_sp = player['speed'][seconds+1]- player['speed'][seconds]

    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3 = st.columns(3)

        # fill in those three columns with respective metrics or KPIs 
        kpi1.metric(label="Time", value=selected_time)
        kpi2.metric(label="Distance", value= f"{round(player_distance,2)}", delta= round(delta_ds,2))
        kpi3.metric(label="Speed", value= f"{round(player_speed,2)}", delta= round(delta_sp,2))

        # create two columns for charts 
        fig_col1, fig_col2 = st.columns(2)
        with fig_col1:
            st.markdown("### First Chart")
            fig = px.scatter(data_frame=player[seconds:seconds+2], y = 'ypos', x = 'xpos')
            st.write(fig)
        with fig_col2:
            st.markdown("### Second Chart")
            img_file = ('./images/player_image'+f'{seconds:02d}'+'.png')
            fig2 = st.image(img_file, caption = "Marked by Martina"+f"{seconds}", use_column_width = 'auto')

        # create data table
        st.markdown("### Detailed Data View")
        st.dataframe(player)
        time.sleep(1)
    #placeholder.empty()

