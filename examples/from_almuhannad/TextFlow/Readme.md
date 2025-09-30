# How to Run the TextFlow API with Docker

This guide explains how to run the TextFlow API application using Docker and Docker Compose on a Linux host.

## Prerequisites

Before you begin, ensure you have the following installed on your Linux machine:
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Running the Application

1.  **Get the Code:**
    Clone the repository or download the source code to a directory on your Linux host. If you don't have a git repository, just make sure all the files (`docker-compose.yml`, `Dockerfile`, `main.py`, etc.) are in the same directory.

2.  **Build and Run with Docker Compose:**
    Open a terminal in the project's root directory (the one containing `docker-compose.yml`) and run the following command:
    ```bash
    docker-compose up --build -d
    ```
    - `--build`: This flag forces Docker Compose to build the images from the Dockerfile.
    - `-d`: This flag runs the containers in detached mode (in the background).

    Docker Compose will now:
    - Build the Docker image for the FastAPI application.
    - Pull the MySQL image.
    - Create and start the application and database containers.
    - Set up the necessary network for the containers to communicate.

3.  **Verify the Application is Running:**
    You can check the status of the running containers with:
    ```bash
    docker-compose ps
    ```
    You should see two services running: `app` and `db`.

## Accessing the API

The API will be accessible on port 8080 of your Linux host.

-   **API Documentation (Swagger UI):**
    Open your web browser and navigate to:
    `http://<your_linux_host_ip>:8080/docs`

-   **Using `curl`:**
    You can send a POST request to the `/convert-measurements` endpoint from your terminal:
    ```bash
    curl -X POST "http://<your_linux_host_ip>:8080/convert-measurements" \
    -H "Content-Type: application/json" \
    -d '{"input_string": "a"}'
    ```
    Replace `<your_linux_host_ip>` with the actual IP address of your Linux machine. If you are running this on your local machine, you can use `localhost`.

## Stopping the Application

To stop the application and remove the containers, run the following command in the project's root directory:
```bash
docker-compose down
```
