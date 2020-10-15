####
## BUIDLER
####
#FROM python:3.6.12-alpine3.12 as builder
#
#WORKDIR /usr/src/app
#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1
#RUN apk update \
#    && apk add python3-dev musl-dev \
#    ca-certificates gcc postgresql-dev linux-headers \
#    libffi-dev jpeg-dev zlib-dev
#RUN pip install --upgrade pip
#COPY . .
#COPY requirements.txt ./
#RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt
#
#
#
#
##########
## FINAL #
##########
#
## pull official base image
#FROM python:3.6.12-alpine3.12
#
## create directory for the app user
#RUN mkdir -p /home/app
#
## create the app user
#RUN addgroup -S app && adduser -S app -G app
#
## create the appropriate directories
#ENV HOME=/home/app
#ENV APP_HOME=/home/app/web
#RUN mkdir $APP_HOME
#WORKDIR $APP_HOME
#
## install dependencies
#RUN apk update && apk add libpq postgresql-dev gcc python3-dev musl-dev
#
#COPY --from=builder /usr/src/app/wheels /wheels
#COPY --from=builder /usr/src/app/requirements.txt .
#RUN pip install --no-cache /wheels/*
#
## copy project
#COPY . $APP_HOME
#
## chown all the files to the app user
#RUN chown -R app:app $APP_HOME
#
## change to the app user
#USER app









FROM python:3.7-buster

# install nginx
RUN apt-get update && apt-get install vim -y --no-install-recommends

# copy source and install dependencies
RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/backend
WORKDIR /opt/app
COPY . /opt/app
RUN pip install -r requirements.txt






# test 1
#FROM python:3.7-buster
#
## install nginx
#RUN apt-get update && apt-get install -y --no-install-recommends
#
## copy source and install dependencies
#RUN mkdir -p /home/app
#COPY requirements.txt ./
#WORKDIR /opt/app
#RUN pip install -r requirements.txt
#


# test 2
# FROM python:3.6.12-alpine3.12
# RUN apk update \
#     && apk add python3-dev musl-dev \
#     ca-certificates gcc postgresql-dev linux-headers \
#     libffi-dev jpeg-dev zlib-dev

# RUN mkdir app
# ADD requirements.txt /app/requirements.txt
# WORKDIR /app
# RUN set -ex \
#     && apk add --no-cache --virtual .build-deps postgresql-dev build-base gcc python3-dev musl-dev libpq \
#     && python -m venv /env \
#     && /env/bin/pip install --upgrade pip \
#     && /env/bin/pip install --no-cache-dir -r /app/requirements.txt \
#     && runDeps="$(scanelf --needed --nobanner --recursive /env \
#     | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
#     | sort -u \
#     | xargs -r apk info --installed \
#     | sort -u)" \
#     && apk add --virtual rundeps $runDeps \
#     && apk del .build-deps

# ADD backend /app

