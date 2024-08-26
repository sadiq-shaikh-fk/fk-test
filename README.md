# YouTube Data API Integration with Quart, Celery, Redis, and Postgres

This project integrates the YouTube Data API to retrieve and store channel and video data using **Quart** (an async Flask alternative) as the API framework, **Celery** for background task processing, **Redis** as the task broker, and **Postgres** for persistent storage.

## Features

- **Asynchronous API** using Quart for non-blocking I/O operations.
- **Task Queues** using Celery and Redis to handle background tasks like fetching data from the YouTube API.
- **YouTube Data API Integration** for fetching channel and playlist data.
- **Postgres Database** for storing retrieved channel and video information.
- **Dockerized Deployment** with Docker Compose for easy setup and scalability.
- **Scalable Architecture** supporting horizontal scaling of Celery workers.
- **Monitoring and Logging** using Prometheus and Grafana for metrics and alerting.

## Project Structure

```plaintext
project/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── tasks.py
│   ├── api_functions.py
│   ├── database.py
│   ├── config.py
│   ├── logging_config.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .env
