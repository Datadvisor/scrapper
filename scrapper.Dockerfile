FROM python:3.9-slim-buster

ARG API_PORT=80

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN apt update
RUN pip3 install -r requirements.txt
RUN apt -y install ffmpeg libsm6 libxext6  -y
RUN apt -y install poppler-utils
RUN apt -y install tesseract-ocr
RUN apt -y install libtesseract-dev

RUN echo "$API_PORT"

ENV API_PORT_RUNTIME=$API_PORT

COPY . /app

CMD ["sh", "-c", "uvicorn src.api.api:app --host 0.0.0.0 --port ${API_PORT_RUNTIME}"]