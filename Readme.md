# Blog Application Setup Guide

This repository contains a full-stack blog application with a Django backend API and React frontend. This guide will walk you through setting up both components.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Quick Start with Docker](#quick-start-with-docker)
- [Backend Setup](#backend-setup)
  - [Local Development Setup](#local-development-setup)
  - [Testing the API](#testing-the-api)
- [Frontend Setup](#frontend-setup)
  - [Installation](#installation)
  - [Available Scripts](#available-scripts)
- [Testing](#testing)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Troubleshooting](#troubleshooting)
- [CI/CD Pipeline](#cicd-pipeline)

## Architecture Overview

This application consists of:
- **Backend**: Django REST API with PostgreSQL database
- **Frontend**: React application created with Create React App
- **Deployment**: Kubernetes orchestration for container management

## Quick Start with Docker

The fastest way to get the entire application running locally is using Docker:

1. Create a project directory and navigate to it:
   ```bash
   mkdir blog-app && cd blog-app
   ```

2. Create a `docker-compose.yml` file:
   ```yaml
   version: '3.8'
   services:
     db:
       image: ajcoder123/postgres:latest
       container_name: postgres-database
       environment:
         POSTGRES_USER: "vipul"
         POSTGRES_PASSWORD: "pawar"
         POSTGRES_DB: "testDB"
       ports:
         - "5435:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
     
     backend:
       image: ajcoder123/backend-web
       container_name: backend-app
       ports:
         - "5000:5000"
       depends_on:
         - db
     
     frontend:
       image: ajcoder123/frontend-web
       container_name: frontend-app
       ports:
         - "3000:3000"
       depends_on:
         - backend
     
     nginx:
       image: nginx:latest
       container_name: nginx-proxy
       ports:
         - "80:80"
       depends_on:
         - backend
         - frontend
       volumes:
         - ./nginx/default.conf:/etc/nginx/conf.d/default.conf

   volumes:
     postgres_data:
       driver: local
   ```

3. Create an Nginx configuration:
   ```bash
   mkdir -p nginx
   ```

4. Create `nginx/default.conf`:
   ```
   server {
       listen 80;
       
       location /api/ {
           proxy_pass http://backend:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location / {
           proxy_pass http://frontend:3000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

5. Start the containers:
   ```bash
   docker-compose up --build -d
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Backend Setup

### Local Development Setup

For local development with more control:

1. **Set up the environment**
   ```bash
   # Clone the repository (if available)
   git clone [repository-url]
   cd [repository-name]/backend
   
   # Create environment file
   cp .env.example .env
   ```

2. **Configure your `.env` file with these variables:**
   ```
   # Environment settings
   DEBUG=True  # Set to False in production

   # PostgreSQL Database
   POSTGRES_USER=your_db_user
   POSTGRES_PASSWORD=your_db_password
   POSTGRES_DB=your_db_name
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432

   # Web Port
   WEB_PORT=5000

   # JWT Token Lifetimes (in minutes)
   ACCESS_TOKEN_LIFETIME=60
   REFRESH_TOKEN_LIFETIME=1440

   # Django Secret Key
   SECRET_KEY=your_django_secret_key

   # Frontend URL
   FRONTEND_URL=your_frontend_url
   ```

3. **Install PostgreSQL:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # MacOS
   brew install postgresql
   brew services start postgresql
   ```

4. **Configure database:**
   ```bash
   # Create a database user
   sudo -u postgres createuser --interactive --pwprompt
   
   # Create a database
   sudo -u postgres createdb your_db_name
   ```

5. **Install Python dependencies:**
   ```bash
   # Install Poetry
   curl -sSL https://install.python-poetry.org | python3 -
   
   # Install dependencies
   poetry shell
   poetry install
   ```

6. **Run migrations and start the server:**
   ```bash
   # Run migrations
   make migrate
   
   # Create a superuser
   make superuser
   
   # Start the server
   make run
   ```

### Testing the API

You can test the API endpoints using Postman:

1. Import the Postman collection (if provided with the project)

2. Configure environment variables:
   - Set the base URL (e.g., `http://localhost:5000`)

3. Authentication flow:
   - Register a new user: `POST /api/auth/register/`
   - Login to get token: `POST /api/auth/login/`
   - Use the token for authenticated requests

4. Test the endpoints:
   - Get all posts: `GET /api/posts/`
   - Create a post: `POST /api/posts/`
   - Get a specific post: `GET /api/posts/{id}/`
   - Update a post: `PUT /api/posts/{id}/`
   - Comment on a post: `POST /api/posts/{id}/comments/`

## Frontend Setup

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Available Scripts

In the frontend directory, you can run:

- **`npm start`**: Runs the app in development mode at [http://localhost:3000](http://localhost:3000)
- **`npm run build`**: Builds the app for production in the `build` folder
- **`npm run eject`**: Extracts all configuration files (one-way operation)

## Testing

To run tests for the project:

### Backend Tests
```bash
cd backend
make test
```



## Kubernetes Deployment

This application is deployed to production using Kubernetes:

### Kubernetes Configuration Files

The application uses the following Kubernetes configuration files:
- `deployment.yml` - Defines the deployment configuration for both frontend and backend
- `service.yml` - Defines the services for accessing the applications
- `ingress.yml` - Configures the ingress controller for external access
- `secrets.yml` - Contains sensitive information like database credentials

### Deploying to Kubernetes

To deploy the application to a Kubernetes cluster:

```bash
# Apply all Kubernetes configurations
kubectl apply -f k8s/
```

This single command will apply all the configuration files in the kubernetes directory.

### Verifying the Deployment

After deployment, verify that all resources are running correctly:

```bash
# Check the status of all pods
kubectl get pods

# Check the status of all services
kubectl get services

# Check the status of the ingress
kubectl get ingress

# Check the deployment status
kubectl get deployments
```

## Troubleshooting

### Backend Issues
- **Database connection errors**: Check your PostgreSQL settings and credentials
- **Port conflicts**: Ensure ports 5000 and 80 are available
- **Migrations failing**: Run `make migrate` in the backend directory

### Frontend Issues
- **Node modules errors**: Delete `node_modules` folder and run `npm install`
- **API connection issues**: Check CORS settings in the backend
- **Build errors**: Check console for specific error messages

### Kubernetes Issues
- **Pods in pending state**: Check for resource constraints or PVC issues
- **CrashLoopBackOff errors**: Check container logs with `kubectl logs <pod-name>`
- **Ingress not working**: Verify that the ingress controller is properly installed and configured
- **Service connection issues**: Check service selectors and port configurations

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:

1. **Workflow Process**:
   - Code checkout from repository
   - Python environment setup
   - Dependencies installation with Poetry
   - Code linting with Black
   - Test execution with pytest
   - Docker image building and pushing to Docker Hub
   - Kubernetes deployment to production cluster

2. **Monitoring**:
   - Check workflow status in the GitHub Actions tab
   - Each push to the main branch triggers the workflow automatically

The CI/CD pipeline ensures code quality and automates the deployment process for both frontend and backend components.