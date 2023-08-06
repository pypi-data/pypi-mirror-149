# import liveisstracker
from liveisstracker.issTrack.issTracking import TrackerISS, get_city_location
import click
from datetime import datetime
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import plotly.express as px
import pandas as pd
from time import sleep

def get_iss_location():
    return TrackerISS(silent=True).gps_location

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--get-iss-location','-i', is_flag=True, help="Get the current location of International Space Station + Google MAP URL")
@click.option('--get-iss-speed','-s',is_flag=True, help="Get the current ground speed of International Space Station")
@click.option('--get-country','-c',is_flag=True, help="Get the country above which the ISS is current passing over")
@click.option('--plot-iss','-p',type=click.Path(exists=False), metavar='FILENAME.png', help="Plot the current position of International Space Station on a map")
def main(get_iss_location,get_iss_speed,get_country,plot_iss):
    """
    liveisstracker can get location,speed and pass-over country based on current location of International Space Station
    """

    location = TrackerISS(silent=True).gps_location

    if get_iss_location:
        print(f'Timestamp (UTC): {datetime.utcfromtimestamp(int(location["timestamp"])).strftime("%Y-%m-%d %H:%M:%S")} ISS is at Lat:{location["latitude"]} Lon:{location["longitude"]}')
        print(f'https://maps.google.com/?q={location["latitude"]},{location["longitude"]}&ll={location["latitude"]},{location["longitude"]}&z=4')

    if get_iss_speed:
        location_0 = location
        sleep(2)
        location_1 = TrackerISS(silent=True).gps_location
        time_diff = location_1['timestamp'] - location_0['timestamp']
        distance = geodesic((location_0['latitude'],location_0['longitude']),
                            (location_1['latitude'],location_1['longitude'])).km

        try:
            speed = distance/time_diff*3600 # km/h
        except ZeroDivisionError:
            speed = 0
        except  Exception as e:
            speed = 99999999999

        print(f'Ground Speed of International Space Station is ~ {round(speed,2)} Km/h')

    if get_country:

        geolocator = Nominatim(user_agent="my-application",timeout=3).reverse(f'{location["latitude"]},{location["longitude"]}',language='en')
        
        try:
            country = geolocator.raw['address']['country']
        except KeyError:
            country = 'the ocean'

        print(f'Internaionl Space Station is currently above {country}')

    if plot_iss:
        fig = px.scatter_geo(pd.DataFrame({'lat':[float(location["latitude"])],
                                        'lon':[float(location["longitude"])]}
                                        ),
                                        lat='lat',
                                        lon='lon', 
                                        width=1300, 
                                        height=800)
        fig.write_image(plot_iss)
        print(f'INFO: Map saved as {plot_iss}')



