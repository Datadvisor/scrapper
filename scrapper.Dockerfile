FROM python:3.9-slim-buster

ARG API_PORT=80

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

RUN echo "$API_PORT"

ENV API_PORT_RUNTIME=$API_PORT

COPY . /app

CMD ["sh", "-c", "uvicorn src.api.api:app --host 0.0.0.0 --port ${API_PORT_RUNTIME}"]