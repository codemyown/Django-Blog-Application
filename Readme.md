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

## Quick Start with Docker Hub Images

For a quick start without cloning the repository or setting up the environment manually, you can use the pre-built Docker images from Docker Hub:

1. Create a new directory for your project and navigate to it:
   ```
   mkdir blog-api && cd blog-api
   ```

2. Create a `docker-compose.yml` file with the following content:
   ```yaml
   version: '3.8'
   services:
     db:
       image: ajcoder123/postgres:latest
       container_name: postgres-database
       environment:
         POSTGRES_USER: "vipul"  # do not change it
         POSTGRES_PASSWORD: "pawar"  # do not change it
         POSTGRES_DB: "testDB"  # do not change it
       ports:
         - "5435:5432"  # do not change the creds
     
     web:
       image: ajcoder123/backend-web
       container_name: backend-app
       ports:
         - "5000:5000"
       depends_on:
         - db
     
     nginx:
       image: nginx:latest
       container_name: nginx-proxy
       ports:
         - "80:80"
       depends_on:
         - web
       volumes:
         - ./nginx/default.conf:/etc/nginx/conf.d/default.conf

   volumes:
     postgres_data:
       driver: local
   ```

3. Create a directory for Nginx configuration:
   ```
   mkdir -p nginx
   ```

4. Create a default Nginx configuration file:
   ```
   touch nginx/default.conf
   ```

5. Add the following configuration to `nginx/default.conf`:
   ```
   server {
       listen 80;
       
       location / {
           proxy_pass http://web:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

6. Start the Docker containers:
   ```
   docker-compose up --build -d
   ```

7. The application will be available at:
   - API: http://localhost:5000
   - Web interface (via Nginx): http://localhost

## CI/CD Workflow

This project uses GitHub Actions for continuous integration and deployment. Here's the workflow process:

1. Code Checkout:
   - The workflow checks out the latest code from the repository

2. Python Setup:
   - Sets up the specified Python version (e.g., Python 3.9)
   - Configures the Python environment

3. Dependencies Installation:
   - Installs Poetry for dependency management
   - Installs all project dependencies using Poetry

4. Code Linting:
   - Runs Black code formatter to ensure code style consistency
   - Checks that all code meets the project's style guidelines

5. Test Execution:
   - Runs all test cases with pytest
   - Includes unit tests, integration tests, and API tests
   - Generates test coverage reports

6. Docker Login:
   - Authenticates with Docker Hub using GitHub Secrets
   - Prepares for image push

7. Build and Push Docker Image:
   - Builds the Docker image with the current code
   - Tags the image appropriately (e.g., latest, version number)
   - Pushes the image to Docker Hub repository

You can check the workflow status in the GitHub Actions tab of the repository. Each push to the main branch triggers this workflow automatically.

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

## Testing with Postman

Follow these steps to test the API endpoints using Postman:

1. Import the collection:
   - In Postman, click on "Import" and select the Postman collection file provided with this project

2. Import the environment variables:
   - Click on "Import" again and select the environment variables file
   - This will load all the necessary variables for testing

3. Configure the environment:
   - Set the `host:port` value in the environment variables
   - Make sure to select and activate the environment for the current collection

4. Authentication flow:
   - Navigate to the "Authentication" folder in the Blog API collection
   - First, use the "Register" endpoint with username, email, and password
   - A status code of 201 indicates successful registration
   - Next, use the "Login" endpoint with your username and password

5. Configure token authentication:
   - After successful login, the API will return an access token
   - Configure this token in the Bearer Authentication settings for the collection
   - This will authenticate all subsequent requests

6. Testing Author endpoints:
   - Go to the "Author" section to get or update author details

7. Testing Posts endpoints:
   - Navigate to the "Posts" section to interact with blog posts
   - Use "Get All Posts" to retrieve all published posts
   - Create a new post using "Create Post" with title, content, and image upload
   - View specific posts with "Get Post by ID"
   - View your own posts with "Get My Posts"
   - Update existing posts with "Update Post"

8. Testing Comments:
   - Within the Posts section, you can interact with post comments
   - Add comments to posts using the "Add Comment" endpoint
   - View and manage comments for specific posts

## Troubleshooting

If you encounter any issues, check that:
- Docker is properly installed and running (for Docker setup)
- PostgreSQL is properly installed and running (for local setup)
- All environment variables are correctly set
- No other services are using the specified ports
- Poetry is correctly installed and activated
- Postman environment variables are correctly set and the environment is active