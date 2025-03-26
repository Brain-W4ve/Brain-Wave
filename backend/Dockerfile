FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (to cache them)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the app
COPY . /app

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the migrations and start the Flask app with Gunicorn
CMD ["sh", "-c", "sleep 5 && alembic upgrade head && gunicorn --bind 0.0.0.0:5000 src.app:app"]
