FROM python:3.9-slim-buster

ARG API_PORT=8002

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update
RUN apt -y install build-essential cmake pkg-config -y

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN apt update
RUN apt -y install ffmpeg libsm6 libxext6  -y
RUN apt -y install poppler-utils
RUN apt -y install tesseract-ocr
RUN apt -y install libtesseract-dev

# setup geckodriver for selenium

RUN apt -y install --no-install-recommends ca-certificates curl firefox-esr
RUN rm -rf /var/lib/apt/lists/*
RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz | tar xz -C /usr/local/bin

#

RUN echo "$API_PORT"

ENV API_PORT_RUNTIME=$API_PORT

COPY . /app

CMD ["sh", "-c", "uvicorn src.api.api:app --host 0.0.0.0 --port ${API_PORT_RUNTIME}"]