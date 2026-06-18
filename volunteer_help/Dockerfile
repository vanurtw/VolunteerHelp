FROM python:3.12-slim
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj
ENV PYTHONBUFFERED=1

RUN pip install --upgrade pip

WORKDIR /app/www/volunteer_help

COPY requirements.txt .
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

COPY . .
USER userdj