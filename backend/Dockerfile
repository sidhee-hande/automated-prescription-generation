# Base python package
FROM python:3.10

# Working directory
WORKDIR /backend

# Copy the dependencies
COPY requirements.txt /backend/

# Install the dependencies
RUN pip3 install -r requirements.txt

# Copy the files
COPY . .

# Executable commands
CMD [ "python3", "-m" , "quart", "run", "--host=0.0.0.0"]