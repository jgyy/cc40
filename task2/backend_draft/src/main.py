import json
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

carparks = [
    {
        'car_park_no': 'ACB',
        'address': 'BLK 270/271 ALBERT CENTRE BASEMENT CAR PARK',
        'lat': 1.301417,
        'lng': 103.849769,
        'car_park_type': 'BASEMENT CAR PARK',
        'parking_system': 'ELECTRONIC PARKING',
        'short_term_parking': 'WHOLE DAY',
        'free_parking': 'NO',
        'night_parking': 'YES',
        'car_park_decks': 1,
        'gantry_height': 1.80,
        'car_park_basement': 'Y'
    },
    {
        'car_park_no': 'BBM',
        'address': 'BLK 505-507 BEACH ROAD MULTISTOREY CAR PARK',
        'lat': 1.303416,
        'lng': 103.862247,
        'car_park_type': 'MULTISTOREY CAR PARK',
        'parking_system': 'ELECTRONIC PARKING',
        'short_term_parking': 'WHOLE DAY',
        'free_parking': 'SUN & PH FR 7AM-10.30PM',
        'night_parking': 'YES',
        'car_park_decks': 10,
        'gantry_height': 2.00,
        'car_park_basement': 'N'
    },
]

users = [
    {
        'user_id': 'user1',
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'password123',
        'created_at': datetime(2023, 1, 1, 9, 0).isoformat()
    },
    {
        'user_id': 'user2',
        'username': 'jane_smith',
        'email': 'jane@example.com',
        'password': 'password456',
        'created_at': datetime(2023, 2, 15, 14, 30).isoformat()
    },
]

reservations = [
    {
        'reservation_id': 'res1',
        'user_id': 'user1',
        'car_park_no': 'ACB',
        'license_plate': 'ABC123',
        'start_time': datetime(2023, 6, 1, 9, 0).isoformat(),
        'end_time': datetime(2023, 6, 1, 12, 0).isoformat(),
        'status': 'active'
    },
    {
        'reservation_id': 'res2',
        'user_id': 'user2',
        'car_park_no': 'BBM',
        'license_plate': 'XYZ789',
        'start_time': datetime(2023, 6, 2, 14, 0).isoformat(),
        'end_time': datetime(2023, 6, 2, 18, 0).isoformat(),
        'status': 'completed'
    },
]

parking_rates = [
    {
        'car_park_no': 'ACB',
        'vehicle_type': 'car',
        'time_period': '1 hour',
        'rate': 1.50
    },
    {
        'car_park_no': 'ACB',
        'vehicle_type': 'motorcycle',
        'time_period': '1 hour',
        'rate': 0.75
    },
    {
        'car_park_no': 'BBM',
        'vehicle_type': 'car',
        'time_period': '30 minutes',
        'rate': 1.00
    },
]

availability = [
    {
        'car_park_no': 'ACB',
        'timestamp': datetime(2023, 6, 1, 10, 0).isoformat(),
        'lots_available': 50,
        'total_lots': 100
    },
    {
        'car_park_no': 'ACB',
        'timestamp': datetime(2023, 6, 1, 11, 0).isoformat(),
        'lots_available': 40,
        'total_lots': 100
    },
    {
        'car_park_no': 'BBM',
        'timestamp': datetime(2023, 6, 2, 15, 0).isoformat(),
        'lots_available': 80,
        'total_lots': 200
    },
]

class RequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, status_code, body=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if body:
            self.wfile.write(json.dumps(body).encode())

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/carparks':
            lat = float(query_params.get('lat', [None])[0])
            lng = float(query_params.get('lng', [None])[0])
            radius = int(query_params.get('radius', [1000])[0])
            page = int(query_params.get('page', [1])[0])
            per_page = int(query_params.get('per_page', [20])[0])
            sort_by = query_params.get('sort_by', ['distance'])[0]

            nearby_carparks = [c for c in carparks if self._is_within_radius(c['lat'], c['lng'], lat, lng, radius)]

            if sort_by == 'distance':
                nearby_carparks.sort(key=lambda c: self._calculate_distance(c['lat'], c['lng'], lat, lng))
            elif sort_by == 'lots_available':
                nearby_carparks.sort(key=lambda c: self._get_lots_available(c['car_park_no']), reverse=True)

            start_index = (page - 1) * per_page
            end_index = start_index + per_page
            paginated_carparks = nearby_carparks[start_index:end_index]

            self._send_response(200, {
                'results': paginated_carparks,
                'total_results': len(nearby_carparks),
                'current_page': page,
                'total_pages': (len(nearby_carparks) + per_page - 1)
            })

    def _is_within_radius(self, lat1, lng1, lat2, lng2, radius):
        distance = self._calculate_distance(lat1, lng1, lat2, lng2)
        return distance <= radius

    def _calculate_distance(self, lat1, lng1, lat2, lng2):
        earth_radius = 6371

        lat1_rad = math.radians(lat1)
        lng1_rad = math.radians(lng1)
        lat2_rad = math.radians(lat2)
        lng2_rad = math.radians(lng2)

        dlat = lat2_rad - lat1_rad
        dlng = lng2_rad - lng1_rad

        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = earth_radius * c

        return distance

    def _get_lots_available(self, car_park_no):
        avail = next((a for a in availability if a['car_park_no'] == car_park_no), None)
        return avail['lots_available'] if avail else 0

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length).decode())

        if self.path == '/users':
            # Create a new user
            user_id = f"user{len(users) + 1}"
            user = {
                'user_id': user_id,
                'username': body['username'],
                'email': body['email'],
                'password': body['password'],
                'created_at': datetime.now().isoformat()
            }
            users.append(user)
            self._send_response(201, user)
        elif self.path == '/reservations':
            reservation_id = f"res{len(reservations) + 1}"
            reservation = {
                'reservation_id': reservation_id,
                'user_id': body['user_id'],
                'car_park_no': body['car_park_no'],
                'license_plate': body['license_plate'],
                'start_time': body['start_time'],
                'end_time': body['end_time'],
                'status': 'active'
            }
            reservations.append(reservation)
            self._send_response(201, reservation)
        else:
            self._send_response(404, {'error': 'Invalid endpoint'})

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
