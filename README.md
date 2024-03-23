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
- Run `./venv/bin/python3 src/main.py` to execute the data extraction 
- The output CSV files will be generated in data directory for task1

## Task 2
Located in task2 directory, currently it is all pseudo code for both IAC and backend.

iac (infrastructure as code) and backend directory have separate makefile

## Architecture

Below are the list of possible infrastructures that can be created. Draft in cloudformation.

### mobile-app-api-lambda-database.yaml
Mobile App -> API Gateway -> Lambda -> DynamoDB or Amazon RDS

### mobile-app-api-lambda-storage-caching.yaml
Mobile App -> API Gateway -> Lambda -> S3 (Data Storage) or ElastiCache (Caching)

### mobile-app-api-lambda-kinesis-processing-database.yaml
Mobile App -> API Gateway -> Lambda -> Kinesis Data Streams -> Lambda (Data Processing) -> DynamoDB or Amazon RDS

### carpark-data-s3-lambda-sns.yaml
Carpark Data Source -> S3 -> Lambda -> SNS (Notification Service)

### mobile-app-api-lambda-carpark-availability-details-database.yaml
Mobile App -> API Gateway -> Lambda (Carpark Availability API) -> Lambda (Carpark Details API) -> DynamoDB or Amazon RDS

### mobile-app-api-lambda-eventbridge-data-sync-external-api.yaml
Mobile App -> API Gateway -> Lambda -> EventBridge -> Lambda (Data Sync) -> External API

### mobile-app-api-ecs-fargate-database.yaml
Mobile App -> API Gateway -> Amazon ECS (Fargate) -> DynamoDB or Amazon RDS

### mobile-app-alb-ecs-ec2-database.yaml
Mobile App -> Application Load Balancer -> Amazon ECS (EC2) -> DynamoDB or Amazon RDS

### mobile-app-api-elastic-beanstalk-database.yaml
Mobile App -> Amazon API Gateway -> AWS Elastic Beanstalk -> DynamoDB or Amazon RDS

### mobile-app-appsync-ecs-fargate-database.yaml
Mobile App -> Amazon AppSync (GraphQL) -> Amazon ECS (Fargate) -> DynamoDB or Amazon RDS

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

## Database Schema (NOSQL or SQL):
```json
// Carparks Table in dynamoDB
{
  "TableName": "Carparks",
  "KeySchema": [
    {
      "AttributeName": "car_park_no",
      "KeyType": "HASH"
    }
  ],
  "AttributeDefinitions": [
    {
      "AttributeName": "car_park_no",
      "AttributeType": "S"
    }
  ],
  "ProvisionedThroughput": {
    "ReadCapacityUnits": 5,
    "WriteCapacityUnits": 5
  }
}

// CarparkAvailability Table in dynamoDB
{
  "TableName": "CarparkAvailability",
  "KeySchema": [
    {
      "AttributeName": "car_park_no",
      "KeyType": "HASH"
    },
    {
      "AttributeName": "timestamp",
      "KeyType": "RANGE"
    }
  ],
  "AttributeDefinitions": [
    {
      "AttributeName": "car_park_no",
      "AttributeType": "S"
    },
    {
      "AttributeName": "timestamp",
      "AttributeType": "N"
    }
  ],
  "ProvisionedThroughput": {
    "ReadCapacityUnits": 5,
    "WriteCapacityUnits": 5
  }
}
```

```sql
-- Carparks Table
CREATE TABLE Carparks (
  car_park_no VARCHAR(50) PRIMARY KEY,
  address VARCHAR(255),
  x_coord DECIMAL(10, 8),
  y_coord DECIMAL(10, 8),
  car_park_type VARCHAR(50),
  type_of_parking_system VARCHAR(50),
  short_term_parking VARCHAR(50),
  free_parking VARCHAR(50),
  night_parking VARCHAR(50),
  car_park_decks INT,
  gantry_height DECIMAL(5, 2),
  car_park_basement VARCHAR(50)
);

-- CarparkAvailability Table
CREATE TABLE CarparkAvailability (
  car_park_no VARCHAR(50),
  timestamp BIGINT,
  total_lots INT,
  available_lots INT,
  PRIMARY KEY (car_park_no, timestamp),
  FOREIGN KEY (car_park_no) REFERENCES Carparks(car_park_no)
);
```

## API Documentation: TODO: put this in swagger instead of readme

### Get Available Carparks
Path: /carparks/available

Method: GET

Description: Returns a list of carparks with available parking lots near a given location

Query Parameters:

latitude (required): Latitude coordinate of the user's location or search location

longitude (required): Longitude coordinate of the user's location or search location

radius (optional): Search radius in meters. Default is 500m if not provided.

Responses:

200 OK on success. Response body:
```json
{
  "carparks": [
    {
      "carparkNo": "C12",
      "address": "123 Main St",  
      "latitude": 1.290270,
      "longitude": 103.851959,
      "totalLots": 500,
      "availableLots": 120
    },
    {
      "carparkNo": "J39",  
      "address": "456 Park Ave",
      "latitude": 1.292049, 
      "longitude": 103.853827,
      "totalLots": 220,
      "availableLots": 50  
    }
  ]
}
```
400 Bad Request if latitude or longitude parameters are missing or invalid. Response body:
```json
{
  "error": "Invalid or missing coordinates"
}
```
500 Internal Server Error for unexpected errors

### Get Carpark Details
Path: /carparks/{carparkNo}

Method: GET

Description: Returns details about a specific carpark

Path Parameters:

carparkNo (required): Unique identifier of the carpark

Responses:

200 OK on success. Response body:
```json
{
  "carparkNo": "C12",
  "address": "123 Main St",
  "latitude": 1.290270, 
  "longitude": 103.851959,
  "carParkType": "MULTI-STOREY CAR PARK",
  "parkingSystemType": "ELECTRONIC PARKING",
  "shortTermParking": "WHOLE DAY",
  "nightParking": "YES",  
  "freeParking": "SUN & PH FR 7AM-10.30PM",
  "gantryHeight": 2
}
```
404 Not Found if carpark does not exist

500 Internal Server Error for unexpected errors

### Get Carpark Availability
Path: /carparks/{carparkNo}/availability

Method: GET

Description: Returns the current availability status of a specific carpark

Path Parameters:

carparkNo (required): Unique identifier of the carpark

Responses:

200 OK on success. Response body:
```json
{
  "carparkNo": "C12",
  "totalLots": 500, 
  "availableLots": 120,
  "updateTime": "2023-06-15T10:30:00Z"
}
```
404 Not Found if carpark does not exist

500 Internal Server Error for unexpected errors

### Get Carparks by Address
Path: /carparks/search

Method: GET

Description: Searches for carparks near a given address

Query Parameters:

address (required): Address string to search for

radius (optional): Search radius in meters. Default is 500m if not provided.

Responses:

200 OK on success. Response body same as /carparks/available endpoint

400 Bad Request if address parameter is missing

500 Internal Server Error for unexpected errors

### Reserve Parking Lot
Path: /carparks/{carparkNo}/reserve

Method: POST

Description: Allows user to reserve a parking lot at a carpark

Path Parameters:

carparkNo (required): Unique identifier of the carpark

Request Body:
```json
{
  "lotNo": "A12",
  "plateNo": "SGA1234B",
  "duration": 60
}
```

Responses:

200 OK on successful reservation. Response body:
```json
{
  "reservationId": "R397540",
  "lotNo": "A12",
  "expiresAt": "2023-06-15T11:30:00Z"  
}
```

400 Bad Request if request body is invalid

404 Not Found if carpark or lot does not exist

409 Conflict if lot is already reserved/occupied

500 Internal Server Error for unexpected errors

### Update Parking Lot Status
Path: /carparks/{carparkNo}/lots/{lotNo}

Method: PUT

Description: Allows updating the status of a parking lot (e.g. when vehicle enters/exits). To be called by carpark system.

Path Parameters:

carparkNo (required): Unique identifier of the carpark

lotNo (required): Lot number

Request Body:
```json
{
  "status": "occupied",
  "plateNo": "SGA1234B" 
}
```
Responses:

200 OK on successful update

400 Bad Request if status is invalid

404 Not Found if carpark or lot does not exist

500 Internal Server Error for unexpected errors

### Error Handling:

All endpoints return appropriate HTTP status codes (e.g. 200, 400, 404, 500)

Detailed error messages are provided in the response body for 4xx and 5xx errors

If no available carparks are found, the carparks array in the response will be empty

### Additional Features:

"Chope-ing" of parking lots:

Users can reserve a parking lot for a specific time slot through the mobile app.

The API will update the available lots count in the CarparkAvailability table accordingly.

To enforce the reservation, the system can generate a unique QR code for each reservation, which the user needs to scan at the carpark 
entrance.

If the user doesn't arrive within a specified time window (e.g., 15 minutes), the reservation will be released.
