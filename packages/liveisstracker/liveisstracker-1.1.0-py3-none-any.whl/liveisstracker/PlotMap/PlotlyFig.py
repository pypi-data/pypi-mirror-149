
import plotly.graph_objects as go
from mylogger.iss_logging import logger
import streamlit as st
from issTrack.issTracking import *
from time import sleep
import os
import pytz
from dateutil import tz
from datetime import datetime

# co_ordinate=iss.get_speed_iss_pos()
# latitude=co_ordinate[1][0]
# longitude=co_ordinate[1][1]

def get_plotly_figure(location,token):
    latitude = location[1][0]
    longitude = location[1][1]
    fig = go.Figure(go.Scattermapbox(lat=[str(latitude)],lon=[str(longitude)],mode='markers',marker=go.scattermapbox.Marker(size=14)))
    fig.update_layout(hovermode='closest',mapbox=dict(accesstoken=token,bearing=0, center=go.layout.mapbox.Center(lat=location[1][0],lon=location[1][1]),pitch=0,zoom=0))
    return fig

def get_mapbox_token(env_var_name):

    try:
        mapbox_access_token = open(os.getenv(env_var_name)).read()
        logger.debug(f'MAPBOX Access Token: {mapbox_access_token}')
        return False, mapbox_access_token
    except TypeError:
        logger.error('Not a valid token. MAPBOX chart will be disabled')
        return True, None

def display_pass_statistics(pass_information):
        logger.debug(f'Pass information: {pass_information}')
        if not pass_information == 'failure':
            pass_number = st.selectbox('Select the pass number?',tuple([s+1 for s in range(len(pass_information))]))
            visible_duration = pass_information[pass_number-1]['duration']
            pred_time = pass_information[pass_number-1]['risetime'] # .strftime('%Y-%m-%d %H:%M:%S') GMT

            timezone = st.selectbox('Select timezone?',tuple([s for s in pytz.all_timezones]))
            pred_time_utc = datetime.utcfromtimestamp(pred_time)

            converted_time = pred_time_utc.astimezone(tz.gettz(timezone)).strftime("%Y-%m-%d %H:%M:%S")
            st.markdown(f"<h3 style='text-align: center;'>Visible for {visible_duration} seconds from {converted_time}</h3>",unsafe_allow_html=True)
        else:
            st.write('Not a valid city')

