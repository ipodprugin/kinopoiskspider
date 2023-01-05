# syntax=docker/dockerfile:1

FROM python:3.10-slim-buster

ENV API_KEY=""

COPY . .
WORKDIR /kinopoiskspider
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD ["scrapy", "crawl", "kinopoisk_popular", "-O", "output.json"]