FROM python:3.11-slim as base
WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "neares_truck.wsgi"]