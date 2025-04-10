for Backend

1. For Docker Setup You need to do the setup and first u need to go inside the backend/ folder and run the command.
2. you can see the .env.example just make the .env file and copy all the things .env.example to the .env and put the details 
# Environment settings
DEBUG=True  # Set to False in production

# PostgreSQL Database
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=your_db_host
POSTGRES_PORT=5432

# Web Port
WEB_PORT=web port

# JWT Token Lifetimes (in minutes/days)
ACCESS_TOKEN_LIFETIME=time in minutes
REFRESH_TOKEN_LIFETIME=time in minutes

# Django Secret Key
SECRET_KEY=your_django_secret_key
