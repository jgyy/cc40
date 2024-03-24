import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from datetime import datetime

users_db = {
    "1": {
        "user_id": "1",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "password": "password123",
        "created_at": "2023-06-01T10:00:00"
    },
    "2": {
        "user_id": "2",
        "username": "janedoe",
        "email": "janedoe@example.com",
        "password": "password456",
        "created_at": "2023-06-02T12:30:00"
    }
}

carparks_db = {
    "1": {
        "carpark_id": "1",
        "address": "123 Carpark Street",
        "lat": 37.7749,
        "lng": -122.4194,
        "carpark_type": "multistorey",
        "parking_system": "electronic",
        "short_term_parking": "7AM-10:30PM",
        "free_parking": "SUN & PH FR 7AM-10:30PM",
        "night_parking": "YES",
        "carpark_decks": 5,
        "gantry_height": 2.0,
        "carpark_basement": "Y"
    },
    "2": {
        "carpark_id": "2",
        "address": "456 Parking Avenue",
        "lat": 40.7128,
        "lng": -74.0060,
        "carpark_type": "surface",
        "parking_system": "coupon",
        "short_term_parking": "NO",
        "free_parking": "NO",
        "night_parking": "NO",
        "carpark_decks": 0,
        "gantry_height": 0.0,
        "carpark_basement": "N"
    }
}

reservations_db = {
    "1": {
        "reservation_id": "1",
        "user_id": "1",
        "carpark_id": "1",
        "license_plate": "ABC123",
        "start_time": "2023-06-10T14:00:00",
        "end_time": "2023-06-10T16:00:00",
        "status": "active"
    },
    "2": {
        "reservation_id": "2",
        "user_id": "2",
        "carpark_id": "2",
        "license_plate": "XYZ789",
        "start_time": "2023-06-12T10:00:00",
        "end_time": "2023-06-12T12:00:00",
        "status": "completed"
    }
}

transactions_db = {
    "1": {
        "transaction_id": "1",
        "user_id": "1",
        "carpark_id": "1",
        "reservation_id": "1",
        "amount": 10.0,
        "payment_method": "credit_card",
        "status": "completed",
        "created_at": "2023-06-10T14:05:00"
    },
    "2": {
        "transaction_id": "2",
        "user_id": "2",
        "carpark_id": "2",
        "reservation_id": "2",
        "amount": 8.0,
        "payment_method": "cash",
        "status": "completed",
        "created_at": "2023-06-12T10:10:00"
    }
}

webhooks_db = {
    "1": {
        "webhook_id": "1",
        "url": "https://example.com/webhook",
        "events": ["carpark_availability_update", "reservation_status_change"]
    }
}

def generate_id():
    return str(len(users_db) + len(carparks_db) + len(reservations_db) + len(transactions_db) + len(webhooks_db))

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

def create_user(username, email, password):
    user_id = generate_id()
    user = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "password": password,
        "created_at": get_current_datetime()
    }
    users_db[user_id] = user
    return user

def get_user(user_id):
    return users_db.get(user_id)

def update_user(user_id, username=None, email=None):
    user = users_db.get(user_id)
    if user:
        if username:
            user["username"] = username
        if email:
            user["email"] = email
    return user

def delete_user(user_id):
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False

# Carpark endpoints
def get_carpark(carpark_id):
    return carparks_db.get(carpark_id)

def get_carparks_by_location(lat, lng, radius=1000):
    # Simulated retrieval of carparks within the specified radius
    carparks = list(carparks_db.values())
    return carparks[:10]  # Return the first 10 carparks for testing

# Reservation endpoints
def create_reservation(user_id, carpark_id, license_plate, start_time, end_time):
    reservation_id = generate_id()
    reservation = {
        "reservation_id": reservation_id,
        "user_id": user_id,
        "carpark_id": carpark_id,
        "license_plate": license_plate,
        "start_time": start_time,
        "end_time": end_time,
        "status": "active"
    }
    reservations_db[reservation_id] = reservation
    return reservation

def get_reservation(reservation_id):
    return reservations_db.get(reservation_id)

def update_reservation(reservation_id, license_plate=None, start_time=None, end_time=None):
    reservation = reservations_db.get(reservation_id)
    if reservation:
        if license_plate:
            reservation["license_plate"] = license_plate
        if start_time:
            reservation["start_time"] = start_time
        if end_time:
            reservation["end_time"] = end_time
    return reservation

def cancel_reservation(reservation_id):
    if reservation_id in reservations_db:
        del reservations_db[reservation_id]
        return True
    return False

# Transaction endpoints
def create_transaction(user_id, carpark_id, reservation_id, amount, payment_method):
    transaction_id = generate_id()
    transaction = {
        "transaction_id": transaction_id,
        "user_id": user_id,
        "carpark_id": carpark_id,
        "reservation_id": reservation_id,
        "amount": amount,
        "payment_method": payment_method,
        "status": "pending",
        "created_at": get_current_datetime()
    }
    transactions_db[transaction_id] = transaction
    return transaction

def get_transaction(transaction_id):
    return transactions_db.get(transaction_id)

def process_payment(transaction_id, payment_method, payment_data):
    transaction = transactions_db.get(transaction_id)
    if transaction:
        transaction["payment_method"] = payment_method
        transaction["status"] = "completed"
        return True
    return False

# Webhook endpoints
def register_webhook(url, events):
    webhook_id = generate_id()
    webhook = {
        "webhook_id": webhook_id,
        "url": url,
        "events": events
    }
    webhooks_db[webhook_id] = webhook
    return webhook

def create_carpark_review(carpark_id, user_id, rating, comment):
    review_id = generate_id()
    review = {
        "review_id": review_id,
        "carpark_id": carpark_id,
        "user_id": user_id,
        "rating": rating,
        "comment": comment,
        "created_at": get_current_datetime()
    }
    # Simulated storage of review in the carpark's reviews
    carpark = carparks_db.get(carpark_id)
    if carpark:
        if "reviews" not in carpark:
            carpark["reviews"] = []
        carpark["reviews"].append(review)
    return review

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/carparks":
            self.handle_get_empty_carpark_lots()
        elif self.path.startswith("/carparks/"):
            carpark_id = self.path.split("/")[-1]
            self.handle_get_carpark_details(carpark_id)
        elif self.path.startswith("/users/") and self.path.endswith("/profile"):
            user_id = self.path.split("/")[-2]
            self.handle_get_user_profile(user_id)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        if self.path == "/users":
            self.handle_create_user()
        elif self.path == "/login":
            self.handle_login()
        elif self.path == "/logout":
            self.handle_logout()
        elif self.path == "/refresh-token":
            self.handle_refresh_token()
        elif self.path.startswith("/carparks/") and self.path.endswith("/reviews"):
            carpark_id = self.path.split("/")[-2]
            self.handle_create_carpark_review(carpark_id)
        elif self.path == "/reservations":
            self.handle_create_reservation()
        elif self.path == "/transactions":
            self.handle_create_transaction()
        elif self.path.startswith("/transactions/") and self.path.endswith("/payment"):
            transaction_id = self.path.split("/")[-2]
            self.handle_process_payment(transaction_id)
        elif self.path == "/webhooks":
            self.handle_register_webhook()
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_PUT(self):
        if self.path.startswith("/users/") and self.path.endswith("/profile"):
            user_id = self.path.split("/")[-2]
            self.handle_update_user_profile(user_id)
        elif self.path.startswith("/reservations/"):
            reservation_id = self.path.split("/")[-1]
            self.handle_update_reservation(reservation_id)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_DELETE(self):
        if self.path.startswith("/users/"):
            user_id = self.path.split("/")[-1]
            self.handle_delete_user(user_id)
        elif self.path.startswith("/reservations/"):
            reservation_id = self.path.split("/")[-1]
            self.handle_cancel_reservation(reservation_id)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def handle_get_empty_carpark_lots(self):
        query_params = parse_qs(self.path.split("?")[-1])
        lat = float(query_params.get("lat", [0])[0])
        lng = float(query_params.get("lng", [0])[0])
        radius = int(query_params.get("radius", [1000])[0])

        empty_lots = get_carparks_by_location(lat, lng, radius)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(empty_lots).encode())

    def handle_get_carpark_details(self, carpark_id):
        carpark_details = get_carpark(carpark_id)

        if carpark_details:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(carpark_details).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Carpark not found"}).encode())

    def handle_create_user(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        user = create_user(username, email, password)

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(user).encode())

    def handle_login(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        username = data.get("username")
        password = data.get("password")

        access_token = None
        for user in users_db.values():
            if user["username"] == username and user["password"] == password:
                access_token = generate_id()
                break

        if access_token:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"access_token": access_token}).encode())
        else:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid credentials"}).encode())

    def handle_logout(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"message": "Logged out successfully"}).encode())

    def handle_refresh_token(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        refresh_token = data.get("refresh_token")

        if refresh_token:
            access_token = generate_id()
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"access_token": access_token}).encode())
        else:
            self.send_response(401)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid refresh token"}).encode())

    def handle_get_user_profile(self, user_id):
        user_profile = get_user(user_id)

        if user_profile:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user_profile).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "User not found"}).encode())

    def handle_update_user_profile(self, user_id):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length).decode()
        data = json.loads(put_data)

        username = data.get("username")
        email = data.get("email")

        updated_user_profile = update_user(user_id, username, email)

        if updated_user_profile:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(updated_user_profile).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "User not found"}).encode())

    def handle_delete_user(self, user_id):
        if delete_user(user_id):
            self.send_response(204)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "User not found"}).encode())

    def handle_create_carpark_review(self, carpark_id):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        user_id = data.get("user_id")
        rating = data.get("rating")
        comment = data.get("comment")

        review = create_carpark_review(user_id, carpark_id, rating, comment)

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(review).encode())

    def handle_update_reservation(self, reservation_id):
        content_length = int(self.headers["Content-Length"])
        put_data = self.rfile.read(content_length).decode()
        data = json.loads(put_data)

        license_plate = data.get("license_plate")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        updated_reservation = update_reservation(reservation_id, license_plate, start_time, end_time)

        if updated_reservation:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(updated_reservation).encode())
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Reservation not found"}).encode())

    def handle_cancel_reservation(self, reservation_id):
        if cancel_reservation(reservation_id):
            self.send_response(204)
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Reservation not found"}).encode())

    def handle_create_transaction(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        user_id = data.get("user_id")
        carpark_id = data.get("carpark_id")
        reservation_id = data.get("reservation_id")
        amount = data.get("amount")
        payment_method = data.get("payment_method")

        transaction = create_transaction(user_id, carpark_id, reservation_id, amount, payment_method)

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(transaction).encode())

    def handle_process_payment(self, transaction_id):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        payment_method = data.get("payment_method")
        payment_data = data.get("payment_data")

        if process_payment(transaction_id, payment_method, payment_data):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Payment processed successfully"}).encode())
        else:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Failed to process payment"}).encode())

    def handle_register_webhook(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        url = data.get("url")
        events = data.get("events")

        webhook = register_webhook(url, events)

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(webhook).encode())

    def handle_create_reservation(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode()
        data = json.loads(post_data)

        user_id = data.get("user_id")
        carpark_id = data.get("carpark_id")
        license_plate = data.get("license_plate")
        start_time = data.get("start_time")
        end_time = data.get("end_time")

        reservation = create_reservation(user_id, carpark_id, license_plate, start_time, end_time)

        self.send_response(201)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(reservation).encode())

def main():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print("Starting server on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
