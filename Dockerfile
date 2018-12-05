# Use na official python runtime as parent
From python:3.6.7

# set the working directory to /wordfreq
WORKDIR /wordfreq

# Copy the current directory contents into the container at /app
COPY . /app

# Install packages required
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# make port 80 available
EXPOSE 80

# Run wordfreq.py when the contsainer launches
CMD ["python", "app.py"]
