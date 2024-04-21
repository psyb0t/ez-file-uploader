FROM python:3.9-slim

# Copy the rest of the application
COPY ./app /app

# Set the working directory
WORKDIR /app

# Create the /app/uploads directory
RUN mkdir -p /app/uploads

RUN pip install -r requirements.txt

# Create a nonroot user with a specific user ID
RUN adduser --disabled-password --gecos '' --uid 1000 nonroot

# Change the ownership of the /app directory to the nonroot user
RUN chown -R nonroot:nonroot /app

# Switch to the nonroot user
USER nonroot

# Command to run the application
CMD ["python", "app.py"]
