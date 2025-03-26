
FROM python:latest

WORKDIR /app

COPY requirements.txt /app/
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 50051

CMD ["python", "model_manager.py"]