FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["sh", "-c", "sleep 5 && alembic upgrade head && flask run --host=0.0.0.0 --port=5000"]
