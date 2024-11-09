# Ad Looper Service

A Python-based service for managing and controlling ads on display devices such as coffee machines, billboards, or digital signage systems. The service provides robust tools for handling ads, devices, users, and scheduling.

## Technologies

- Python 3+
- FastAPI
- SQLAlchemy (with asyncpg for asynchronous PostgreSQL operations)
- Alembic for database migrations
- Poetry for dependency management and packaging

## Key Features

- **User Management**: The system supports user registration and authentication. Users can manage their ads and devices, with relationships between users, media, schedules, and tokens.
  
- **Device Management**: The service allows users to associate media and schedules with display devices (e.g., billboards, coffee machines), ensuring dynamic ad content.

- **Ad Scheduling**: Users can schedule ads to run at specific times on display devices, linking media to devices through media groups and schedules.

- **Token System**: A comprehensive token system is implemented to authorize and authenticate users and devices. Tokens are associated with users and devices to manage access and permissions.

## Database Configuration

This service uses PostgreSQL as the backend database with asynchronous operations provided by `asyncpg` and `SQLAlchemy`. The database connection string and other configurations are set in the `settings.py` file.

Database migrations are handled using Alembic.
