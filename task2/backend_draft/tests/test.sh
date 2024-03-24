#!/bin/bash

echo ""
echo "Create a new user:"
curl -X POST -H "Content-Type: application/json" -d '{"username": "newuser", "email": "newuser@example.com", "password": "password789"}' http://localhost:8000/users
echo ""
echo "User login:"
curl -X POST -H "Content-Type: application/json" -d '{"username": "johndoe", "password": "password123"}' http://localhost:8000/login
echo ""
echo "User logout:"
curl -X POST http://localhost:8000/logout
echo ""
echo "Refresh access token:"
curl -X POST -H "Content-Type: application/json" -d '{"refresh_token": "your_refresh_token"}' http://localhost:8000/refresh-token
echo ""
echo "Get user profile:"
curl -X GET http://localhost:8000/users/1/profile
echo ""
echo "Update user profile:"
curl -X PUT -H "Content-Type: application/json" -d '{"username": "johndoe_updated", "email": "johndoe_updated@example.com"}' http://localhost:8000/users/1/profile
echo ""
echo "Delete user account:"
curl -X DELETE http://localhost:8000/users/1
echo ""
echo "Get empty carpark lots:"
curl -X GET "http://localhost:8000/carparks?lat=37.7749&lng=-122.4194&radius=1000"
echo ""
echo "Get carpark details:"
curl -X GET http://localhost:8000/carparks/1
echo ""
echo "Create a carpark review:"
curl -X POST -H "Content-Type: application/json" -d '{"user_id": "1", "rating": 4, "comment": "Great carpark!"}' http://localhost:8000/carparks/1/reviews
echo ""
echo "Create a new reservation:"
curl -X POST -H "Content-Type: application/json" -d '{"user_id": "1", "carpark_id": "1", "license_plate": "ABC456", "start_time": "2023-06-15T09:00:00", "end_time": "2023-06-15T11:00:00"}' http://localhost:8000/reservations
echo ""
echo "Update reservation:"
curl -X PUT -H "Content-Type: application/json" -d '{"license_plate": "DEF789", "start_time": "2023-06-15T10:00:00", "end_time": "2023-06-15T12:00:00"}' http://localhost:8000/reservations/1
echo ""
echo "Cancel reservation:"
curl -X DELETE http://localhost:8000/reservations/1
echo ""
echo "Create a new transaction:"
curl -X POST -H "Content-Type: application/json" -d '{"user_id": "1", "carpark_id": "1", "reservation_id": "1", "amount": 12.5, "payment_method": "credit_card"}' http://localhost:8000/transactions
echo ""
echo "Process payment for a transaction:"
curl -X POST -H "Content-Type: application/json" -d '{"payment_method": "credit_card", "payment_data": {"card_number": "1234567890123456"}}' http://localhost:8000/transactions/1/payment
echo ""
echo "Register a webhook:"
curl -X POST -H "Content-Type: application/json" -d '{"url": "https://example.com/webhook", "events": ["carpark_availability_update", "reservation_status_change"]}' http://localhost:8000/webhooks
