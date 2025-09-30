# String Processor API

This project is a FastAPI-based web service that provides an API for processing strings based on a specific set of rules. The application is containerized using Docker and logs all transactions to a MySQL database and local log files.

## Features

- **FastAPI**: A modern, high-performance web framework for building APIs.
- **Custom String Processing**: Implements a unique and complex set of rules for converting strings into a list of numbers.
- **Containerized Environment**: Uses Docker and Docker Compose for easy setup, deployment, and scalability.
- **Persistent Logging**: Logs every API transaction to a MySQL database.
- **File-Based Logging**: Maintains separate log files for general API events and detailed interactions.

## API Endpoint

### Convert Measurements

Processes a string according to the defined rules and returns a list of numbers.

- **URL**: `/convert-measurements`
- **Method**: `GET`
- **Query Parameters**:
  - `input` (string, required): The string to be processed.

- **Example Request**:
  ```sh
  curl "http://localhost:8080/convert-measurements?input=azb-c"
  ```

- **Example Response**:
  ```json
  {
    "input_string": "azb-c",
    "output": [28, 0, 3]
  }
  ```

## String Processing Rules

The core logic of this application is a custom string processing algorithm with the following rules:

1.  **Lowercase Conversion**: The input string is first converted to lowercase.
2.  **Character Values**:
    - Characters from 'a' to 'z' have values from 1 to 26, respectively.
    - Any character not in the 'a'...'z' range is treated as having a value of 0.
3.  **Sequences**: The string is processed in sequences.
    - If a character's value is 0 (e.g., '-', ' ', '1'), it forms a standalone sequence resulting in the number `0`.
    - A sequence of alphabetic characters is processed as follows:
        1.  **Count Determination**: The sequence starts by determining a `count`. This count is calculated by the value of the first character(s). Chained 'z's are used to build the count (e.g., 'z' = 26, 'zz' = 52, 'zza' = 53).
        2.  **Item Collection**: After the count is determined, the next `count` number of *items* are collected. An item can be a single character or a z-chain (e.g., 'za').
        3.  **Summation**: The character values of all collected items are summed up to produce a single number for the sequence.

## Logging

The application features three distinct logging mechanisms for comprehensive monitoring:

1.  **MySQL Database Logging**: Every API request and its corresponding response are logged as a new entry in the `request_logs` table in the `api_logs_db` database.
2.  **API Log (`log_config.py`)**: General API events and information are logged to a daily log file located at `logs/api_YYYYMMDD.log`.
3.  **Interaction Log (`interaction_logger.py`)**: Detailed request and response data for each transaction is logged to `logs/interactions.log`.

## Prerequisites

To run this project, you must have the following installed:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

1.  **Clone the Repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Build and Run with Docker Compose**:
    Open a terminal in the project's root directory and run the following command:
    ```sh
    docker-compose up --build
    ```
    This command will:
    - Build the Docker image for the FastAPI application.
    - Start the MySQL database container.
    - Start the FastAPI application container.

3.  **Access the API**:
    The API will be running and available at `http://localhost:8585`. You can access the interactive documentation at `http://localhost:8585/docs`.

## Project Structure

```
.
├── Dockerfile              # Defines the Docker image for the FastAPI app
├── docker-compose.yml      # Configures and runs the application and database services
├── init.sql                # SQL script to initialize the database schema
├── log_config.py           # Configures the general API file logger
├── interaction_logger.py   # Configures the interaction-specific file logger
├── logsql.py               # Handles logging to the MySQL database
├── main.py                 # The main FastAPI application file
├── README.md               # This file
└── requirements.txt        # Python dependencies
```
"# Final-Evaluation" 
