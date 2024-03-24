import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime

carparks = [
    {
        'car_park_no': 'ACB',
        'address': 'BLK 270/271 ALBERT CENTRE BASEMENT CAR PARK',
        'lat': 30314.7936,
        'lng': 31490.4942,
        'car_park_type': 'BASEMENT CAR PARK',
        'parking_system': 'ELECTRONIC PARKING',
        'short_term_parking': 'WHOLE DAY',
        'free_parking': 'NO',
        'night_parking': 'YES',
        'car_park_decks': 1,
        'gantry_height': 1.80,
        'car_park_basement': 'Y'
    },
]

users = [
    {
        'user_id': 'user1',
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'password123',
        'created_at': datetime.now().isoformat()
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
]

parking_rates = [
    {
        'car_park_no': 'ACB',
        'vehicle_type': 'car',
        'time_period': '1 hour',
        'rate': 1.50
    },
]

availability = [
    {
        'car_park_no': 'ACB',
        'timestamp': datetime(2023, 6, 1, 10, 0).isoformat(),
        'lots_available': 50,
        'total_lots': 100
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
            # Retrieve carparks based on query parameters
            # Implement pagination, sorting, and filtering logic
            self._send_response(200, carparks)
        elif path.startswith('/carparks/'):
            car_park_no = path.split('/')[-1]
            if path.endswith('/availability'):
                # Retrieve current availability for a specific carpark
                avail = next((a for a in availability if a['car_park_no'] == car_park_no), None)
                if avail:
                    self._send_response(200, avail)
                else:
                    self._send_response(404, {'error': 'Availability data not found'})
            elif path.endswith('/availability/historical'):
                # Retrieve historical availability data for a specific carpark
                # Implement date range and interval filtering logic
                historical_data = [a for a in availability if a['car_park_no'] == car_park_no]
                self._send_response(200, historical_data)
            elif path.endswith('/pricing'):
                # Retrieve pricing information for a specific carpark
                pricing = [p for p in parking_rates if p['car_park_no'] == car_park_no]
                self._send_response(200, {'parking_rates': pricing})
            else:
                # Retrieve a specific carpark by car_park_no
                carpark = next((c for c in carparks if c['car_park_no'] == car_park_no), None)
                if carpark:
                    self._send_response(200, carpark)
                else:
                    self._send_response(404, {'error': 'Carpark not found'})
        elif path.startswith('/users/'):
            user_id = path.split('/')[-1]
            if path.endswith('/reservations'):
                # Retrieve reservations made by a specific user
                user_reservations = [r for r in reservations if r['user_id'] == user_id]
                self._send_response(200, user_reservations)
            else:
                # Retrieve a specific user by user_id
                user = next((u for u in users if u['user_id'] == user_id), None)
                if user:
                    self._send_response(200, user)
                else:
                    self._send_response(404, {'error': 'User not found'})
        elif path.startswith('/reservations/'):
            reservation_id = path.split('/')[-1]
            # Retrieve a specific reservation by reservation_id
            reservation = next((r for r in reservations if r['reservation_id'] == reservation_id), None)
            if reservation:
                self._send_response(200, reservation)
            else:
                self._send_response(404, {'error': 'Reservation not found'})
        else:
            self._send_response(404, {'error': 'Invalid endpoint'})

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
            # Create a new reservation
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
