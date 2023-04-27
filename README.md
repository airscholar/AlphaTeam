# Alpha Team App

This is the repository for the Alpha Team App.
The application is a web application that allows users to visualise and analyse complex networks.
The application is built using Flask.

## Running the application locally

1. Clone the repository
2. Navigate to the backend directory and run
    - `export FLASK_APP=app.py` for Linux/Mac or `set FLASK_APP=app.py` for Windows
3. Run `flask run --host=0.0.0.0 --port=8000` to start the backend server
4. Open another terminal and navigate to the application directory
5. Run `flask run --host=0.0.0.0 --port={chosen port}` to start the frontend server
6. Open your browser and go to `http://127.0.0.1:{chosen port}`

# Docker Setup

Install Docker and Docker Compose on your machine. You can find the
instructions [here](https://docs.docker.com/install/).

## Running the application using Docker

1. Clone the repository
2. Run `docker build -t alpha-team .` in the root directory of the project to build the Docker image
3. Run `docker run -d -p 8000:8000 -p 3000:3000 --name alpha-team alpha-team` to start the application
3. Open your browser and go to `http://127.0.0.1:3000`
4. Enjoy!

# Documentation

On the frontend of the application, you can find the documentation for the API endpoints once the frontend application
is started at `http://localhost:{chosen port}/docs`
