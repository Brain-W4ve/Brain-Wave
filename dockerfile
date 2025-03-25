FROM python:3.10-alpine

WORKDIR /app

RUN apk add --no-cache \
    postgresql-libs \
    gcc \
    python3-dev \
    musl-dev \
    postgresql-dev \
    libffi-dev


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD ["sh", "-c", "sleep 5 && alembic upgrade head && python app.py"]
