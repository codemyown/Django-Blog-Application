# Backend Setup Guide

## Environment Setup

Before proceeding with either Docker or local setup, you need to configure your environment:

1. Navigate to the backend directory:
   ```
   cd backend/
   ```

2. Create your environment file:
   - Copy the contents from `.env.example` to a new file named `.env`
   ```
   cp .env.example .env
   ```
   - Update the following configuration values in the .env file:

   ```
   # Environment settings
   DEBUG=True  # Set to False in production

   # PostgreSQL Database
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=your_db_name
   POSTGRES_HOST=your_db_host  # Use 'localhost' for local setup
   POSTGRES_PORT=5432

   # Web Port
   WEB_PORT=your_web_port

   # JWT Token Lifetimes (in minutes/days)
   ACCESS_TOKEN_LIFETIME=time_in_minutes
   REFRESH_TOKEN_LIFETIME=time_in_minutes

   # Django Secret Key
   SECRET_KEY=your_django_secret_key
   ```

## Docker Setup Instructions

Follow these steps to set up the backend using Docker:

1. Build and start the Docker containers:
   ```
   docker-compose up --build -d
   ```

2. Access the application:
   - Open your browser or Postman and navigate to `localhost:5000` (or your configured port)
   - For Postman usage, set up environment variables with the appropriate values

3. Please let me know if any error occurs during the setup process.

## Local Development Setup

Follow these steps for a local development environment:

1. Install PostgreSQL and Beekeeper (optional):
   ```
   # For Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # For MacOS using Homebrew
   brew install postgresql
   
   # Start PostgreSQL service
   # Ubuntu/Debian
   sudo systemctl start postgresql
   # MacOS
   brew services start postgresql
   ```
   
   You can download Beekeeper Studio (a database management tool) from the [official website](https://www.beekeeperstudio.io/).

2. Configure PostgreSQL:
   ```
   # Create a new database user
   sudo -u postgres createuser --interactive --pwprompt
   
   # Create a new database
   sudo -u postgres createdb your_db_name
   ```

3. For local setup, make sure to set `POSTGRES_HOST=localhost` in your .env file.

4. Install Python and Poetry:
   ```
   # Install Python (if not already installed)
   # Ubuntu/Debian
   sudo apt install python3 python3-pip
   
   # MacOS
   brew install python
   
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -
   ```

5. Activate Poetry shell:
   ```
   poetry shell
   ```

6. Install dependencies:
   ```
   poetry install
   ```

7. Run the application:
   ```
   # Run database migrations
   make migrate
   
   # Start the server
   make run
   
   # Create a superuser
   make superuser
   ```

8. Testing commands:
   ```
   # Run all tests
   make test
   
   # Run unit tests only
   make test-unit
   
   # Run integration tests only
   make test-integration
   
   # Run API tests only
   make test-api
   ```

## Troubleshooting

If you encounter any issues, check that:
- Docker is properly installed and running (for Docker setup)
- PostgreSQL is properly installed and running (for local setup)
- All environment variables are correctly set
- No other services are using the specified ports
- Poetry is correctly installed and activated