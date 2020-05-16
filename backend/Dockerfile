FROM python:3.8.2

WORKDIR /usr/src/words

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/words/requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . /usr/src/words

