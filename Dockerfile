# syntax=docker/dockerfile:1.2
FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements-dev.txt requirements-test.txt ./

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt \
    && pip install --no-cache-dir -r requirements-test.txt \
    && pip install --no-cache-dir xgboost jupyter "anyio<4.0.0"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "challenge.api:app", "--host", "0.0.0.0", "--port", "8000"]
