import unittest
import os
from urllib.request import urlretrieve
from src.main import load_json_data, load_xlsx_data, extract_restaurants, extract_restaurant_events, get_rating_thresholds

class TestRestaurantData(unittest.TestCase):
    def setUp(self):
        self.data_folder = 'test_data'
        os.makedirs(self.data_folder, exist_ok=True)
        
        self.restaurant_data_file = os.path.join(self.data_folder, 'restaurant_data.json')
        url = 'https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json'
        urlretrieve(url, self.restaurant_data_file)
        
        self.country_codes_file = os.path.join(self.data_folder, 'Country-Code.xlsx')
        country_codes_url = 'https://github.com/Papagoat/brain-assessment/blob/main/Country-Code.xlsx?raw=true'
        urlretrieve(country_codes_url, self.country_codes_file)

    def tearDown(self):
        os.remove(self.restaurant_data_file)
        os.remove(self.country_codes_file)
        os.rmdir(self.data_folder)

    def test_load_json_data(self):
        data = load_json_data(self.restaurant_data_file)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_load_xlsx_data(self):
        data = load_xlsx_data(self.country_codes_file)
        self.assertIsInstance(data, dict)
        self.assertIn(1, data)

    def test_extract_restaurants(self):
        data = load_json_data(self.restaurant_data_file)
        country_codes = load_xlsx_data(self.country_codes_file)
        restaurants = extract_restaurants(data, country_codes)
        self.assertIsInstance(restaurants, list)
        self.assertGreater(len(restaurants), 0)

    def test_extract_restaurant_events(self):
        data = load_json_data(self.restaurant_data_file)
        events = extract_restaurant_events(data)
        self.assertIsInstance(events, list)

    def test_get_rating_thresholds(self):
        data = load_json_data(self.restaurant_data_file)
        thresholds = get_rating_thresholds(data)
        self.assertIsInstance(thresholds, dict)

if __name__ == '__main__':
    unittest.main()
