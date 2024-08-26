FROM python:3.12-alpine

WORKDIR /code

RUN pip install Flask psycopg2-binary

COPY . .

EXPOSE 5000

CMD ["python","-m", "shiri_hamelech"]
