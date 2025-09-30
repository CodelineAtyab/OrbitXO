# Package Measurement Conversion API

## Overview
This project implements a **Package Measurement Conversion API** using **FastAPI** and **MySQL**.  
The API converts measurement input strings into a list of total values of measured inflows for each package.  

The application is containerized using **Docker** and can be run on any Linux or Windows host via **docker-compose**.

---

## Features

- **Conversion Endpoint**:  
  `GET /convert-measurements?input=<string>`  
  Converts the input string into a list of total values per package.

- **History Endpoint**:  
  `GET /history`  
  Returns all previously converted inputs and their results from the database.

- **Logging**:  
  All logs are written to `logs/app.log`.

- **Database**:  
  MySQL is used to store conversion history. The schema is initialized automatically from `sql/init.sql`.

- **Custom Port**:  
  You can run the API on any port by passing it as an argument:  
  ```bash
  python main_app.py 8888
