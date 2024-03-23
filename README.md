## Task 1
Located in task1 directory, run make or python3 command there

If python is not installed, download python [here](https://www.python.org/downloads/)

### Manual Setup and run
- `cd task1` change to this directory
- Create a virtual environment: `python3 -m venv venv` 
- Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On Mac/Linux: `source venv/bin/activate` 
- Install required packages: `pip install -r requirements.txt`
- `./venv/bin/python3 src/main.py` Execute the python script

### Setup Mac/Linux or windows wsl with Makefile
- `make` run this command to create environment and run python script
- `make run` execute python script
- `make test` to run unit tester
- `make fclean` cleanup the python environment

### Running the Code manually
- Make sure the virtual environment is activated
- Run `python3 main.py` to execute the data extraction 
- The output CSV files will be generated in data directory for task1

## Task 2
Located in task2 directory, currently it is all pseudo code for both IAC and backend.

## Makefile
WIP, added to attempt to create aws resources

## Architecture

### Serverless Architecture with Data Processing:
```txt
Mobile App -> API Gateway -> Lambda -> DynamoDB
                                    -> S3 (Data Storage)
                                    -> Kinesis Data Streams -> Lambda (Data Processing) -> DynamoDB
``` 

### Serverless Architecture with Caching:
```txt
Mobile App -> API Gateway -> Lambda -> DynamoDB
                                    -> ElastiCache (Caching)
```

### Serverless Architecture with Event-Driven Updates:
```txt
Mobile App -> API Gateway -> Lambda -> DynamoDB
                                    -> SNS (Notification Service)
Carpark Data Source -> S3 -> Lambda -> DynamoDB
                                    -> SNS (Notification Service)
```

### Serverless Architecture with API Composition:
```txt
Mobile App -> API Gateway -> Lambda (Carpark Availability API) -> DynamoDB
                                                               -> Lambda (Carpark Details API) -> DynamoDB
```

### Serverless Architecture with EventBridge:
```txt
Mobile App -> API Gateway -> Lambda -> DynamoDB
                                    -> EventBridge -> Lambda (Data Sync) -> External API
```

## System Design

- From mobile app send HTTP Request
- Invoke Backend Server
1. Parse Request
2. Validate Request
3. Determine User Location
   - Extract location from request payload
   - If location not provided, use default location
4. Retrieve Nearby Carparks
   - Query database based on user location
   - Use GSI (Global Secondary Index) for efficient querying
   - Apply radius filter to get carparks within a certain distance
5. Filter Available Carparks
   - Iterate over retrieved carparks
   - Check availability status of each carpark
   - Filter out carparks with no available lots
6. Retrieve Carpark Details
   - For each available carpark, retrieve additional details
   - Query database Carpark Details table
   - Enrich the response with carpark details
7. Prepare Response
   - Format the response payload
   - Include carpark availability and details
8. Return Response
   - Send the response back to the API Gateway
- HTTP Response back to mobile app

## Database Schema (DynamoDB):

### Table: Carparks
- car_park_no (Partition Key, String)
- address (String)
- x_coord (Number)
- y_coord (Number)
- car_park_type (String)
- type_of_parking_system (String)
- short_term_parking (String)
- free_parking (String)
- night_parking (String)
- car_park_decks (Number)
- gantry_height (Number)
- car_park_basement (String)

### Table: CarparkAvailability
- car_park_no (Partition Key, String)
- timestamp (Sort Key, Number)
- total_lots (Number)
- available_lots (Number)

## API Documentation:

### GET /carparks/nearby
Description: Retrieves a list of nearby carparks with available parking lots based on user's location.

Query Parameters:

latitude (required): User's latitude coordinate

longitude (required): User's longitude coordinate

radius (optional, default 1000): Search radius in meters

Response:

200 OK: Returns a list of nearby carparks with available parking lots

400 Bad Request: Invalid or missing parameters

### GET /carparks/search

Description: Retrieves a list of carparks with available parking lots based on user input location.

Query Parameters:

location (required): User input location (e.g., postal code, address)

Response:

200 OK: Returns a list of carparks with available parking lots near the input location

400 Bad Request: Invalid or missing parameters

### Error Handling:

If the user inputs a non-existing location or invalid coordinates, the API will return a 400 Bad Request response with an appropriate error message.

If no carparks are found within the specified radius or near the input location, the API will return an empty list.

### Additional Features:

"Chope-ing" of parking lots:

Users can reserve a parking lot for a specific time slot through the mobile app.

The API will update the available lots count in the CarparkAvailability table accordingly.

To enforce the reservation, the system can generate a unique QR code for each reservation, which the user needs to scan at the carpark 
entrance.

If the user doesn't arrive within a specified time window (e.g., 15 minutes), the reservation will be released.
