"""
Author: Manoj Manivannan
Date 13-Jun-2020

This script plots the ground position of international space station on a spherical map.
The location of ISS is obtained from 'http://api.open-notify.org/iss-now.json'
The resulting Geo coordinates are plot using matplotlib.
"""


import time
import streamlit as st
from mylogger.iss_logging import logger
from issTrack.page_information import information
from issTrack.issTracking import *
from PlotMap.MapBasePlot import *
from PlotMap.PlotlyFig import get_plotly_figure, get_mapbox_token, display_pass_statistics

st.set_page_config(
    page_title="Live ISS Tracker", 
    page_icon='https://icons.iconarchive.com/icons/goodstuff-no-nonsense/free-space/512/international-space-station-icon.png', 
    layout='centered', 
    initial_sidebar_state='auto')


def main():
            
    try:
        st.title('International Space Station Tracker')
        st.markdown(information['header1'])
        st.markdown(information['what'])
        st.markdown(information['intro_source'],unsafe_allow_html=True)
        st.markdown(information['header2'])
        st.markdown(information['tech_spec'], unsafe_allow_html=True)
        st.markdown(information['intro_source'],unsafe_allow_html=True)

        iss = TrackerISS()
        live_show = st.radio("Show live tracking in orthographic",('Yes', 'No'), index=1)
        if live_show == 'Yes':
            home_name_st = st.text_input('Distance relative to (city)',value='')
            if home_name_st:
                home_name, home_lat, home_lon = get_city_location(home_name_st)
                
                earth = BasemapPlot(home_name,home_lat,home_lon)
        while live_show == 'Yes' and home_name_st:
            earth.plot_location(iss.get_speed_iss_pos())
            with st.spinner('Reloading in 5 seconds..'):
                time.sleep(5)

        mapbox_disable,mapbox_access_token = get_mapbox_token(env_var_name='MAPBOX_TOKEN')
        if not mapbox_disable:        
            st.write("Current ISS location in flat view")
            location = iss.get_speed_iss_pos()
            fig = get_plotly_figure(location,token=mapbox_access_token)

            if st.button('Refresh'):
                pass
            st.plotly_chart(fig)

        st.write("Predict next ISS pass through by city")
        predict_city = st.text_input('Enter city name',value='London')
        
        if predict_city:
            _, predict_city_lat, predict_city_lon = get_city_location(predict_city)

            pass_information=iss.get_pass_info_from_lat_lon(predict_city_lat,predict_city_lon)
            display_pass_statistics(pass_information)


    except Exception as e:
        logger.error('Failed {}'.format(e))
        raise Exception(e)


if __name__ == '__main__':
    main()