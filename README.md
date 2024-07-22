# AI Communication Gateway Service

## Overview
This project is a processing service built with FastAPI and SQLAlchemy. 
It allows client to send messages to various AI providers and receive responses, 
with token-based authentication.

## Features
- Multiple AI provider support
- Easily extendable to integrate with various AI providers
- Utilizes asynchronous database operations, HTTP clients, and application logic to ensure high performance and responsiveness
- Docker support for easy deployment
- Configurable with environment variables
- Token-based authentication

## Prerequisites
- Docker (for containerized deployment)
- Non-containerized deployment with this configuration might require additional setup (Not recommended!).

## Installation

### Local Setup
1. Clone the repository.
2. Ensure you have a .env file or have filled in the required variables in the docker-compose.yml. 
Read the next section for the list of required environment variables.
3. Run: 
```shell
docker compose up --build
```

### Environment Variables
1. Create .env or fill docker-compose with following variables:
    - POSTGRES_DB=<your_postgres_db>
    - POSTGRES_USER=<your_postgres_user>
    - POSTGRES_PASSWORD=<your_postgres_password>
    - POSTGRES_POOL_SIZE=<your_postgres_pool_size>
    - POSTGRES_MAX_OVERFLOW=<your_postgres_max_overflow>
    
    - APP_RUN_HOST=<your_app_run_host>
    - APP_RUN_PORT=<your_app_run_port>
    - DEBUG=<0_or_1>
    
    - TOKEN_EXPIRATION_MINUTES=<your_token_expiration_minutes>
    - #### TOKEN_EXPIRATION_DAYS (WARNING: for now unused)
    - #### PGADMIN_DEFAULT_EMAIL (WARNING: pgadmin only for dev, not for prod)
    - #### PGADMIN_DEFAULT_PASSWORD (WARNING: pgadmin only for dev, not for prod)
    

### Get a token
1. Go to docker container environment and run (not from here!):
```shell
python3 scripts/generate_token.py
```

## Contact
Written by Ivan Aleksandrovskii
Email: i.aleksandrovskii@chrona.ai