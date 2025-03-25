FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
# COPY ./src /app/src
COPY . /app
# COPY ./migrations /app/migrations
# COPY .env /app/.env
# COPY ./alembic.ini /app/alembic.ini
# COPY ./requirements.txt /app/requirements.txt

# Install any dependencies in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the migrations and start the Flask app with Gunicorn
CMD ["sh", "-c", "sleep 5 && alembic upgrade head && gunicorn --bind 0.0.0.0:5000 src.app:app"]