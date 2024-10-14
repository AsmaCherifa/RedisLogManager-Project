# Log Management System

## Overview

This project implements a log management system using Redis for storage and Elasticsearch for indexing, enabling efficient log retrieval and analysis.
It also includes a log generator script to simulate log entries and demonstrate the system's functionality.


## Features
- Generates random log entries for testing purposes.
- Stores log entries in Redis using unique IDs.
- Filters and displays logs based on log type (e.g., "ERROR").
- Sets expiration (1 hour) for error logs.
- Counts and displays the number of logs by type (INFO, ERROR, WARNING).
- Store logs in Elasticsearch.
- Visualization of log data in Kibana.

## Requirements

- Python
- Redis
- Elasticsearch
- Kibana



## Usage

1. Run the Python script:
    ```bash
    python script_log_redis.py
    ```

2. The script will read the `app_logs.txt` file, parse it, and store each log in Redis. It will also display the logs in the console and show a count of logs by type.

