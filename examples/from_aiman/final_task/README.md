# API Request/Response Logging Service

## Summary

This project is a containerized FastAPI application designed to automatically log the details of every API request and its corresponding response to a MySQL database. The entire environment is orchestrated using Docker and Docker Compose, making it portable and easy to deploy.

## How It Works

The application's logic is centered around a custom FastAPI middleware that intercepts all HTTP traffic, logs it, and then forwards it to the intended endpoint. The entire process is managed by Docker Compose.

1.  **Docker Compose Orchestration (`docker-compose.yml`)**:
    *   When you run `docker-compose up`, two services are defined and created: `db` and `app`.
    *   The `app` service `depends_on` the `db` service, ensuring the database is running before the application attempts to connect.
    *   **`db` Service**: This service uses the official `mysql:8.0` image. Environment variables (`MYSQL_ROOT_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`) are used by the MySQL image's entrypoint script to automatically create the `log_db` database and the `username` user on initial startup.
    *   **`app` Service**: This service builds a Docker image from the local `Dockerfile`. It receives the database connection details via environment variables, which are used by the application at runtime to connect to the `db` service. The `volumes` mapping (`.:/app`) mounts the local project directory into the container, allowing for live code changes without rebuilding the image.

2.  **Database Initialization (`mysql-init/init.sql`)**:
    *   The `docker-compose.yml` file mounts the `mysql-init` directory into `/docker-entrypoint-initdb.d` inside the `db` container.
    *   This is a special directory recognized by the official MySQL image. Any `.sql` scripts placed here are automatically executed when the database container is first created.
    *   Our `init.sql` script runs after the `log_db` database has been created. It first issues a `USE log_db;` command to select the correct database. It then executes a `CREATE TABLE IF NOT EXISTS requests_log (...)` statement to create the table that will store the API logs.

3.  **Middleware Interception (`main.py`)**:
    *   The core of the logging logic resides in a FastAPI middleware, defined in `main.py` using the `@app.middleware("http")` decorator.
    *   A middleware is a function that processes every request before it reaches the endpoint and every response before it is sent to the client. It acts as a wrapper around the entire request-response lifecycle.

4.  **Data Capture & Logging (`main.py` & `logsql.py`)**:
    *   **Request Capture**: The middleware function receives the incoming `request`. It reads the request body using `await request.body()` and captures other details like the URL, method, and headers.
    *   **Processing**: It then calls `response = await call_next(request)`. This passes control to the actual API endpoint (e.g., the function handling the `/` route), which processes the request and generates a `response` object.
    *   **Response Capture**: Once the endpoint is done, the middleware resumes. It reads the response body from the `response.body_iterator` and captures the status code.
    *   **Database Logging**: With all the request and response data collected, the middleware calls the `log_interaction` method from the `db_logger` instance (imported from `logsql.py`).
    *   **`DatabaseLogger` Class (`logsql.py`)**: This class handles the database connection. Its `log_interaction` method connects to the MySQL database (using credentials from the environment variables), constructs an `INSERT` SQL statement with the captured data, and executes it to create a new record in the `requests_log` table. It uses `with` statements to ensure the database connection and cursor are always closed properly, even if errors occur.

## Core Technologies

This project relies on several key Python libraries to function:

*   **FastAPI**: A modern, high-performance web framework for building APIs with Python. It is used to create the API endpoints and to define the middleware that intercepts and logs requests. Its use of standard Python type hints provides data validation and automatic interactive documentation.

*   **Uvicorn**: An ASGI (Asynchronous Server Gateway Interface) server used to run the FastAPI application. It's lightweight and extremely fast. The `[standard]` installation option is used, which includes libraries like `uvloop` and `httptools` for even better performance. Uvicorn is the production-ready server that listens for HTTP requests and passes them to the FastAPI application.


## Deployment Instructions

### Prerequisites

*   [Docker](https://www.docker.com/get-started)
*   [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Navigate to the Project Directory**:
    Open a terminal and change the directory to the project's root folder.

2.  **Build and Run the Containers**:
    Execute the following command. This will build the application image and start the FastAPI and MySQL services in the background.

    ```bash
    docker-compose up --build -d
    ```

### Verifying the Setup

1.  **Check Running Containers**:
    Ensure both services are running with the command:
    ```bash
    docker ps
    ```
    You should see two containers listed: one for the `app` and one for the `db`.

2.  **Test the API Endpoint**:
    Send a request to the application. You can use a web browser to navigate to `http://localhost:8080` or use a tool like `curl`:
    ```bash
    curl http://localhost:8080
    ```
    You should receive the response: `{"message":"Hello World"}`.

3.  **Check the Database Log**:
    Connect to the MySQL database using any SQL client (like SQLTools in VS Code, DBeaver, or the command line).
    *   **Host**: `localhost` or `127.0.0.1`
    *   **Port**: `3306`
    *   **User**: `username`
    *   **Password**: `password`
    *   **Database**: `log_db`

    Query the `requests_log` table to see the record of your API call:
    ```sql
    SELECT * FROM requests_log;
    ```

### Stopping the Application

*   To stop the services, run:
    ```bash
    docker-compose down
    ```
*   To stop the services and **delete all database data**, run:
    ```bash
    docker-compose down -v
    ```