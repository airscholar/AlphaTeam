# Dockerfile for AlphaTeam

# BUILD: docker build -t alphateam .
# RUN: docker run -p 8000:8000 -p 5000:5000 --name alphateam-container alphateam

# /!\ WARNING /!\
# FOR NOW REPOSITORY IS PRIVATE SO IT WILL NOT WORK

# Use official Python 3.10 image as base
FROM python:3.10

# Set the working directory
WORKDIR /AlphaTeam

# Clone the Github repository
RUN git clone git@github.com:airscholar/AlphaTeam.git .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports
EXPOSE 8000 5000

# Start the backend API
CMD ["sh", "-c", "python backend/app.py &"]

# Start the application
CMD ["python", "application/app.py"]
