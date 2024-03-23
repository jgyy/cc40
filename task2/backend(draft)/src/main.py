import csv
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

class CarparkRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/carparks'):
            self.get_available_carparks()
        else:
            self.send_error(404, 'Not Found')

    def do_POST(self):
        if self.path.startswith('/carparks') and self.path.endswith('/reserve'):
            self.reserve_parking_lot()
        else:
            self.send_error(404, 'Not Found')

    def get_available_carparks(self):
        latitude = self.get_query_param('latitude')
        longitude = self.get_query_param('longitude')
        location = self.get_query_param('location')

        carpark_data = []
        with open('HDBCarparkInformation.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                carpark_data.append(row)

        if latitude is None or longitude is None:
            if location is None:
                self.send_error(400, 'Missing latitude, longitude, or location')
                return
            else:
                # Handle location-based search
                available_carparks = []
                for carpark in carpark_data:
                    if location.lower() in carpark['address'].lower():
                        available_carparks.append({
                            'id': carpark['car_park_no'],
                            'name': carpark['address'],
                            'latitude': carpark['y_coord'],
                            'longitude': carpark['x_coord'],
                            'total_lots': carpark['car_park_type'],
                            'available_lots': 'N/A',
                            'last_updated': 'N/A'
                        })
        else:
            # Handle latitude/longitude-based search
            available_carparks = []
            for carpark in carpark_data:
                if float(latitude) - 0.01 <= float(carpark['y_coord']) <= float(latitude) + 0.01 and \
                float(longitude) - 0.01 <= float(carpark['x_coord']) <= float(longitude) + 0.01:
                    available_carparks.append({
                        'id': carpark['car_park_no'],
                        'name': carpark['address'],
                        'latitude': carpark['y_coord'],
                        'longitude': carpark['x_coord'],
                        'total_lots': carpark['car_park_type'],
                        'available_lots': 'N/A',
                        'last_updated': 'N/A'
                    })

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(available_carparks).encode())

    def reserve_parking_lot(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        carpark_id = self.path.split('/')[-2]
        user_id = data.get('user_id')
        duration = data.get('duration')

        if not user_id or not duration:
            self.send_error(400, 'Missing user_id or duration')
            return

        carpark_data = []
        with open('HDBCarparkInformation.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                carpark_data.append(row)

        carpark = next((c for c in carpark_data if c['car_park_no'] == carpark_id), None)

        if not carpark:
            self.send_error(404, 'Carpark not found')
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Reservation successful'}).encode())

    def get_query_param(self, param):
        query = self.path.split('?')[-1]
        params = dict(qc.split('=') for qc in query.split('&') if '=' in qc)
        return params.get(param)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CarparkRequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
