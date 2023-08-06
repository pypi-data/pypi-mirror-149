from mpl_toolkits.basemap import Basemap # pip does not include this package, install by downloading the binary from web
import matplotlib.pyplot as plt
plt.rcParams['animation.ffmpeg_path'] = '/usr/bin/ffmpeg' # point to the extracted exe file of ffmpeg
import matplotlib.animation as animate
import streamlit as st
from issTrack.issTracking import TrackerISS
from mylogger.iss_logging import logger
import numpy as np
from geopy.geocoders import Nominatim

class BasemapPlot:

    def __init__(self, home_name,home_latitude, home_longitude):

        self.home_name = home_name
        self.home_latitude = home_latitude
        self.home_longitude = home_longitude

        # self.gps_location = gps_location

        figure, ax = plt.subplots(num="ISS Tracker",figsize=(14,8))
        self.the_plot = st.pyplot(plt,clear_figure=True)

    def create_plot(self):
        self.gps_location = TrackerISS.get_iss_lat_lon()

        try:
            self.m = Basemap(projection='ortho',
                lat_0=self.gps_location['latitude'],
                lon_0=self.gps_location['longitude'],
                resolution='c')
            self.m.fillcontinents(color='coral',lake_color='aqua')
            # draw parallels and meridians
            self.m.drawparallels(np.arange(-90.,91.,30.))
            self.m.drawmeridians(np.arange(-180.,181.,60.))
            self.m.drawcountries()
            self.m.drawmapboundary(fill_color='aqua')
            return self
        except Exception as e:
            print('Failure in basemap',e)

    def plot_location(self, speed_iss_pos):

        speed = speed_iss_pos[0]
        iss = speed_iss_pos[1]

        self.create_plot()
        x_pt, y_pt = self.m(self.gps_location['longitude'],self.gps_location['latitude'])
        self.point = self.m.plot(x_pt, y_pt,'bo')[0]
        self.point.set_data(x_pt,y_pt)
        plt.text(x_pt, y_pt, 'Lat:{} Lon:{}'.\
            format(\
                round(self.gps_location['latitude'],2),\
                round(self.gps_location['longitude'],2)))

        distance_to_home = TrackerISS.get_distance_btwn_locations(location_1 = (self.home_latitude, self.home_longitude),\
                                                                    location_2 = iss)
         
        location = Nominatim(user_agent="my-application",timeout=3)\
        .reverse('{},{}'.format(self.gps_location['latitude'],\
            self.gps_location['longitude']), language='en')
        try:
            country = location.raw['address']['country']
        except KeyError:
            country = 'the ocean'

        plt.title('ISS is currently above {} \n \
            Ground distance between {} and ISS is {}km.\n \
            Ground speed {} km/h' \
            .format(country,self.home_name,round(distance_to_home,2),round(speed,2) if speed > 1 else 'Calculating...'))
        self.the_plot.pyplot(plt,clear_figure=True)