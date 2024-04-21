FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Create the /app/uploads directory
RUN mkdir /app/uploads

# Install packages from requirements.txt
# Doing this before copying the entire application can leverage Docker cache
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . /app

# Create a nonroot user with a specific user ID
RUN adduser --disabled-password --gecos '' --uid 1000 nonroot

# Change the ownership of the /app directory to the nonroot user
RUN chown -R nonroot:nonroot /app

# Switch to the nonroot user
USER nonroot

# Command to run the application
CMD ["python", "app.py"]
