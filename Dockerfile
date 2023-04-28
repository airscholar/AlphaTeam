FROM ubuntu:latest

# Install python3 and pip3 and other dependencies
RUN apt-get update -y && apt-get install -y python3-pip python3-dev\
    build-essential libssl-dev libffi-dev python3-setuptools && \
    apt-get install -y python3-venv && apt-get install -y python3-wheel && \
    apt-get install -y python3-cffi && apt-get install -y libpq-dev

# Install GDAL dependencies
RUN apt-get install -y binutils libproj-dev gdal-bin && apt-get install -y libgdal-dev && \
    apt-get install -y python3-gdal && apt-get install -y python3-pip && \
    apt-get install -y graphviz graphviz-dev

# Export the environment variables for GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Set the working directory
WORKDIR /alpha-team

# Install GDAL and pygraphviz
RUN pip install GDAL pygraphviz
RUN pip3 install torch --index-url https://download.pytorch.org/whl/cpu
# Copy the current directory contents into the container at /AlphaTeam
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /AlphaTeam
COPY . .

# Expose the ports
EXPOSE 8000
EXPOSE 3000

#change to backend folder
WORKDIR /alpha-team

# set flask environment variables
ENV FLASK_APP=app.py

# Start the application
CMD (cd backend && flask run --host 0.0.0.0 --port 8000 > backend.log 2>&1 &) && \
    (cd application && flask run --host 0.0.0.0 --port 3000 > frontend.log 2>&1 &) && \
    tail -f backend/backend.log application/frontend.log




