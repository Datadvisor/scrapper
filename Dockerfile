FROM python:3.9-slim-buster

ENV GRPC_PORT=8002

WORKDIR /app

RUN apt-get update
RUN apt-get -y install  \
    build-essential \
    ca-certificates \
    cmake \
    curl \
    ffmpeg  \
    firefox-esr \
    libsm6  \
    libxext6  \
    pkg-config \
    poppler-utils  \
    tesseract-ocr  \
    libtesseract-dev
RUN rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz | tar xz -C /usr/local/bin

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /app

ENTRYPOINT ["python"]

CMD ["main.py"]