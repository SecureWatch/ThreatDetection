# Backend Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirement.txt

ENV FLASK_APP=app.py
EXPOSE 5000

CMD ["python", "app.py"]