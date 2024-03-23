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

## API Documentation
cd to ./task2/swagger and run make command, after that go to browser and
visit http://localhost:8080 to see swagger website on carpark api
