FROM python:3

ENV PYTHONUNBUFFERED=1

WORKDIR /app

ADD . /app

COPY ./requirements.txt /app/requirements.txt

EXPOSE 8000
EXPOSE 25
EXPOSE 587

RUN pip install -r requirements.txt

COPY . /app