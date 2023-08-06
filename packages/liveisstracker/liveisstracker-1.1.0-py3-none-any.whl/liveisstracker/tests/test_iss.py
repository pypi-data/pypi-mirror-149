from unittest import TestCase, TextTestRunner, defaultTestLoader
from liveisstracker.issTrack.issTracking import TrackerISS
from urllib.error import URLError

###### MODENA #######################
home_name="MODENA"
home_lat=44.6501557
home_lon=10.8516923

class TestISSTracker(TestCase):

    @classmethod
    def setUpClass(self):
        print("Test ISS Tracker Start")
        self.tracker = TrackerISS()


    @classmethod
    def tearDownClass(self):
        print("Test ISS Tracker  Done")

    def test_default_assertTrue(self):
        # print("Default Test")
        self.assertTrue(True)

    def test_get_speed_iss_at_0_0(self):
        # print("Speed test speed=0")
        self.tracker.timestamp_pre = 0
        testing_mode = {'timestamp':1, 'latitude':0, 'longitude':0}
        self.assertEqual(self.tracker.get_speed_iss_pos(testing_mode = testing_mode)[0],0)

    def test_get_speed_iss_at_1_1(self):
        # print("Speed test iss at 1,1")
        self.tracker.timestamp_pre = 0
        self.tracker.lon_pre = 0
        self.tracker.lat_pre = 0
        testing_mode = {'timestamp':1, 'latitude':1, 'longitude':1}
        self.assertAlmostEqual(self.tracker.get_speed_iss_pos(testing_mode = testing_mode)[0],564838.4, places=1)

    def test_get_speed_iss_at_10_10(self):
        self.tracker.timestamp_pre = 0
        self.tracker.lon_pre = 0
        self.tracker.lat_pre = 0
        testing_mode = {'timestamp':1, 'latitude':10, 'longitude':10}
        self.assertAlmostEqual(self.tracker.get_speed_iss_pos(testing_mode = testing_mode)[0],5634392.7, places=0)

    def test_get_iss_location_invalid_link(self):
        # print("Fetch ISS location - Invalid link")
        testing_mode = {'iss_link':'http://api.open-notify.org/iss-no.json'}
        self.assertRaises(URLError, self.tracker.get_iss_lat_lon, testing_mode)

    def test_get_iss_distance_from_location_0_0_km(self):
        #
        testing_mode = {'location_1':(0,0), 'location_2':(0,0)}
        self.assertEqual(self.tracker.get_distance_btwn_locations(testing_mode=testing_mode),0)

    def test_get_iss_distance_from_location_1_1_km(self):
        #
        testing_mode = {'location_1':(0,0), 'location_2':(1,1)}
        self.assertAlmostEqual(self.tracker.get_distance_btwn_locations(testing_mode=testing_mode),156.89, places=1)

    def test_get_iss_distance_from_location_10_10_km(self):

        testing_mode = {'location_1':(0,0), 'location_2':(10,10)}
        self.assertAlmostEqual(self.tracker.get_distance_btwn_locations(testing_mode=testing_mode),1565.1, places=1)

    def test_get_pass_information_from_location_0_0(self):
        testing_mode={'timestamp':1, 'latitude':0, 'longitude':0}
        self.assertEqual(self.tracker.get_pass_info_from_lat_lon(testing_mode=testing_mode),'failure')

def run():
    TextTestRunner().run(defaultTestLoader.loadTestsFromTestCase(TestISSTracker))

if __name__ == '__main__':

    run()

