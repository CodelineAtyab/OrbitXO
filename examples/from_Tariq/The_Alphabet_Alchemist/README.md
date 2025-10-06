
<<<<<<< HEAD
A FastAPI microservice that provides an API for a custom string-to-number conversion algorithm. The service logs all requests to both a file and a MySQL database.

## Description

The Alphabet Alchemist is a microservice built with FastAPI that exposes a single endpoint for processing strings based on a complex set of rules. It converts an input string into a list of numbers. The application is fully containerized using Docker and Docker Compose, including a MySQL database for persistent logging of requests and responses.

## Features

*   **Custom String Processing**: Implements a unique algorithm to convert strings into a list of integers.
*   **Dual Logging**: Logs every API transaction to both a rotating log file (`/logs/api.log`) and a `requests_log` table in a MySQL database.
*   **Containerized**: Ready to run with Docker Compose, which sets up the application and a persistent MySQL database.

## API Endpoint

The service exposes a single endpoint running on port 8080.

*   `GET /convert-measurements`: Processes an input string according to the custom algorithm.
    *   **Query Parameter**: `input` (string) - The string to be processed.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have Docker and Docker Compose installed on your machine.

*   [Docker Desktop](https://www.docker.com/products/docker-desktop)

### Running with Docker Compose

The project is configured to run with Docker Compose. The `docker-compose.yml` file will build and run the FastAPI application and a MySQL database service.

1.  **Clone the repository (if you haven't already):**

    ```bash
    git clone <your-repository-url>
    cd aiops-The-Alphabet-Alchemist
    ```

2.  **Prepare the database initialization script:**

    The `docker-compose.yml` file references a `./mysql-init` directory to initialize the database. Create this directory and a SQL script inside it.

    Create a directory named `mysql-init`:
    ```bash
    mkdir mysql-init
    ```

    Create a file named `mysql-init/init.sql` with the following content to create the necessary table for logging:
    ```sql
    CREATE TABLE IF NOT EXISTS requests_log (
        id INT AUTO_INCREMENT PRIMARY KEY,
        timestamp VARCHAR(255) NOT NULL,
        input_string TEXT,
        output_data TEXT
    );
    ```

3.  **Build and run the application:**

    Open a terminal in the project's root directory and run the following command:

    ```bash
    docker-compose up --build -d
    ```

    This command will:
    *   Build the Docker image for the application.
    *   Pull the MySQL image.
    *   Start both containers.
    *   Create a `logs` directory on your host for file-based logs.

4.  **Verify the application is running:**

    You can check the status of the running containers with:

    ```bash
    docker-compose ps
    ```

    You should see both the `app` and `db` containers in an "up" state.

## Usage

Once the application is running, you can send requests to the `/convert-measurements` endpoint.

**Example using `curl`:**

```bash
curl -X GET "http://localhost:8080/convert-measurements?input=a_b_c"
```

**Expected response:**

```json
{
  "input_string": "a_b_c",
  "output": [
    0,
    3
  ]
}
```

After making a request, you can check the logs:
*   **File Log**: A new `logs` directory will be created in your project root. Check the `api.log` file inside it.
*   **Database Log**: You can connect to the MySQL database on `localhost:3306` (user: `your_username`, password: `your_password`) and query the `requests_log` table in the `api_log_db` database.

## Stopping the application

To stop and remove the containers, run the following command in the project's root directory:

```bash
docker-compose down
```

To also remove the persistent database volume, use:
```bash
docker-compose down -v
```
```bash
docker-compose down -v
```
=======
>>>>>>> 2099f650f6070847258a7ddc4665efb14f5f07cb
