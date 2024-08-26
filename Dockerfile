FROM python:3.12-alpine

WORKDIR /code

RUN pip install Flask psycopg2

COPY . .

EXPOSE 5000

CMD ["python","shiri_hamelech"]
