# Assumptions
This README assumes that the user is either using macos, linux or wsl to execute the program as commands such as `make` is unavailable in cmd and powershell for windows. User also need docker installed in their PC in order to test swagger app.

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
- `make lint` run flake8 linter to make sure the python script conform to PEP8 standard.

### Running the Code manually
- Make sure the virtual environment is activated
- Run `./venv/bin/python3 src/main.py` to execute the data extraction 
- The output CSV files will be generated in data directory for task1

### Code Explaination

- Overview
  - The python script extract restaurant data and events from [restaurant_data.json](https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json)
  - Map country codes to country names using [Country-Code.xlsx](https://github.com/Papagoat/brain-assessment/blob/main/Country-Code.xlsx?raw=true)
  - Determine rating thresholds based on aggregate ratings via `def get_rating_thresholds(data):`.
  - Save the extracted data as restaurant_events.csv and restaurants.csv
  - Libraries used: os, csv, json, datetime, urllib.request, openpyxl

- Data Loading
  - `def load_json_data(file_path):` Loads data from a JSON file
  - `def load_xlsx_data(file_path):` Loads data from an Excel file using openpyxl library, Maps country codes to country names

- `def extract_restaurants(data, country_codes):`
  - Extracts relevant fields from the restaurant data
  - Maps rating text to rating categories
  - Stores the extracted data in a list of dictionaries

- `def extract_restaurant_events(data):`
  - Extracts events for restaurants in April 2019
  - Stores the extracted event data in a list of dictionaries

- `def write_csv(file_path, data, fieldnames):`
  - Writes the extracted data to a CSV file
  - Uses the csv library to create a DictWriter

- `def get_rating_thresholds(data):`
  - Calculates the thresholds for different rating categories
  - Based on the unique aggregate ratings in the data

- `if __name__ == '__main__':`
  - Downloads the JSON and Excel files.
  - Loads the data using `load_json_data` and `load_xlsx_data`.
  - Extracts restaurants and events data
  - Writes the extracted data to restaurant_events.csv and restaurants.csv.
  - Prints the rating thresholds.
```sh
User Aggregate Rating Thresholds:
Excellent: 4.9 - 4.9
Very Good: 4.8 - 4.9
Good: 4.7 - 4.8
Average: 4.6 - 4.7
Poor: 0.0 - 4.6
```

## Task 2
Located in task2 directory, there are 3 directories, iac_draft, backend_draft and swagger

iac (infrastructure as code) directory stores all the cloudformation pseudo script for deploying the backend api.

backend directory stores the python backend server as a proof of concept for the API, not fully implemented.

swagger directory do have the working swagger app, make sure you have docker installed in the system and just run `make` command.

### Architecture

Below are the list of possible infrastructures that can be created. Draft in cloudformation.

```txt
mobile-app-api-lambda-database.yaml
Mobile App -> API Gateway -> Lambda -> DynamoDB or Amazon RDS

mobile-app-api-lambda-storage-caching.yaml
Mobile App -> API Gateway -> Lambda -> S3 (Data Storage) or ElastiCache (Caching)

mobile-app-api-lambda-kinesis-processing-database.yaml
Mobile App -> API Gateway -> Lambda -> Kinesis Data Streams -> Lambda (Data Processing) -> DynamoDB or Amazon RDS

carpark-data-s3-lambda-sns.yaml
Carpark Data Source -> S3 -> Lambda -> SNS (Notification Service)

mobile-app-api-lambda-carpark-availability-details-database.yaml
Mobile App -> API Gateway -> Lambda (Carpark Availability API) -> Lambda (Carpark Details API) -> DynamoDB or Amazon RDS

mobile-app-api-lambda-eventbridge-data-sync-external-api.yaml
Mobile App -> API Gateway -> Lambda -> EventBridge -> Lambda (Data Sync) -> External API

mobile-app-api-ecs-fargate-database.yaml
Mobile App -> API Gateway -> Amazon ECS (Fargate) -> DynamoDB or Amazon RDS

mobile-app-alb-ecs-ec2-database.yaml
Mobile App -> Application Load Balancer -> Amazon ECS (EC2) -> DynamoDB or Amazon RDS

mobile-app-api-elastic-beanstalk-database.yaml
Mobile App -> Amazon API Gateway -> AWS Elastic Beanstalk -> DynamoDB or Amazon RDS

mobile-app-appsync-ecs-fargate-database.yaml
Mobile App -> Amazon AppSync (GraphQL) -> Amazon ECS (Fargate) -> DynamoDB or Amazon RDS
```

## System Design
can refer to backend directory to see the python http server also.

1. From mobile app send HTTP Request
2. Invoke Backend Server
3. Parse Request
4. Validate Request
5. Determine User Location
   - Extract location from request payload
   - If location not provided, use default location
6. Retrieve Nearby Carparks
   - Query database based on user location
   - Use GSI (Global Secondary Index) for efficient querying
   - Apply radius filter to get carparks within a certain distance
7. Filter Available Carparks
   - Iterate over retrieved carparks
   - Check availability status of each carpark
   - Filter out carparks with no available lots
8. Retrieve Carpark Details
   - For each available carpark, retrieve additional details
   - Query database Carpark Details table
   - Enrich the response with carpark details
9. Prepare Response
   - Format the response payload
   - Include carpark availability and details
10. Return Response
   - Send the response back to the API Gateway
11. HTTP Response back to mobile app

### Database Schema:
I am assuming sql for simplicity sake as nosql data structure are more or less similar.

```sql
CREATE TABLE carparks (
    car_park_no VARCHAR(10) PRIMARY KEY,
    address VARCHAR(255) NOT NULL,
    lat DECIMAL(10, 8) NOT NULL,
    lng DECIMAL(11, 8) NOT NULL,
    car_park_type VARCHAR(50) NOT NULL,
    parking_system VARCHAR(50) NOT NULL,
    short_term_parking VARCHAR(50),
    free_parking VARCHAR(50),
    night_parking VARCHAR(10),
    car_park_decks INTEGER,
    gantry_height DECIMAL(4, 2),
    car_park_basement VARCHAR(1)
);

CREATE TABLE users (
    user_id VARCHAR(50) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reservations (
    reservation_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    car_park_no VARCHAR(10) NOT NULL,
    license_plate VARCHAR(20) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(10) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (car_park_no) REFERENCES carparks(car_park_no)
);

CREATE TABLE parking_rates (
    car_park_no VARCHAR(10),
    vehicle_type VARCHAR(20),
    time_period VARCHAR(50),
    rate DECIMAL(8, 2),
    PRIMARY KEY (car_park_no, vehicle_type, time_period),
    FOREIGN KEY (car_park_no) REFERENCES carparks(car_park_no)
);

CREATE TABLE availability (
    car_park_no VARCHAR(10),
    timestamp TIMESTAMP,
    lots_available INTEGER,
    total_lots INTEGER,
    PRIMARY KEY (car_park_no, timestamp),
    FOREIGN KEY (car_park_no) REFERENCES carparks(car_park_no)
);
```

### API Documentation

cd to ./task2/swagger and run make command (docker required), after that go to browser and
visit http://localhost:8080 to see swagger website on carpark api
