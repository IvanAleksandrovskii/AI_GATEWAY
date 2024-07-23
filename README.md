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

1. Create a `.env` file or fill in the `docker-compose` file with the following variables:

   - **PostgreSQL Configuration:**
     - `POSTGRES_DB=<your_postgres_db>`
       - The name of your PostgreSQL database.
       - Example: `POSTGRES_DB=postgres_db`
     - `POSTGRES_USER=<your_postgres_user>`
       - The username for connecting to your PostgreSQL database.
       - Example: `POSTGRES_USER=user`
     - `POSTGRES_PASSWORD=<your_postgres_password>`
       - The password for connecting to your PostgreSQL database.
       - Example: `POSTGRES_PASSWORD=password`
     - `POSTGRES_POOL_SIZE=<your_postgres_pool_size>`
       - The size of the connection pool for PostgreSQL. This determines how many connections are maintained to the database.
       - Example: `POSTGRES_POOL_SIZE=5`
     - `POSTGRES_MAX_OVERFLOW=<your_postgres_max_overflow>`
       - The maximum number of connections that can be created above the pool size.
       - Example: `POSTGRES_MAX_OVERFLOW=10`
    
   - **Application Configuration:**
     - `APP_RUN_HOST=<your_app_run_host>`
       - The host on which the application will run.
       - Example: `APP_RUN_HOST=0.0.0.0`
     - `APP_RUN_PORT=<your_app_run_port>`
       - The port on which the application will run.
       - Example: `APP_RUN_PORT=8000`
     - `DEBUG=<0_or_1>`
       - Enable or disable debug mode. Use `1` to enable and `0` to disable.
       - Example: `DEBUG=0`

   - **Authentication Configuration:**
     - `TOKEN_EXPIRATION_DAYS=<your_token_expiration_days>`
       - The number of days before the authentication token expires.
       - Example: `TOKEN_EXPIRATION_DAYS=30`

   - **HTTP Client Management Configuration:**
     - `HTTP_CLIENT_TIMEOUT=<your_http_client_timeout_in_seconds>`
       - Example: `HTTP_CLIENT_TIMEOUT=300`
     - `HTTP_CLIENTS_MAX_KEEPALIVE_CONNECTIONS=<your_max_keepalive_clients_count>`
       - Example: `HTTP_CLIENTS_MAX_KEEPALIVE_CONNECTIONS=10`

  - **pgAdmin Configuration (Development Only)**
    **Note**: pgAdmin should only be used in a development environment and not in production.
    - `PGADMIN_DEFAULT_EMAIL=<your_pgadmin_email>`
      - The default email address for pgAdmin login.
      - Example: `PGADMIN_DEFAULT_EMAIL=admin@example.com`
    - `PGADMIN_DEFAULT_PASSWORD=<your_pgadmin_password>`
      - The default password for pgAdmin login.
      - Example: `PGADMIN_DEFAULT_PASSWORD=admin_password`


### Get a token
1. Go to docker container environment and run (not from here!):
```shell
python3 scripts/generate_token.py
```

## Contact
Written by Ivan Aleksandrovskii
Email: i.aleksandrovskii@chrona.ai