FROM python:3.11.2-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . .   
EXPOSE 8003
