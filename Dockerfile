# pull official base image
FROM python:3.8.5-alpine



# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1


# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN apk add --update --no-cache postgresql-client python3-dev \
 libffi-dev jpeg-dev freetype-dev libjpeg-turbo-dev libpng-dev \
 curl jq

RUN apk add --update --no-cache --virtual .tmp-build-deps \
 gcc g++ libc-dev linux-headers postgresql-dev musl-dev zlib \
 zlib-dev
# RUN pip install cloudinary django-cloudinary-storage
RUN pip install -r requirements.txt
# RUN pip install gunicorn
# RUN pip install whitenoise
RUN apk del .tmp-build-deps

# RUN pip install -r requirements.txt

# copy project
# COPY . .
COPY ./fixmycity_api /app
WORKDIR /app


# RUN mkdir /app
# WORKDIR /app
# COPY ./fixmycity_api .


# COPY ./entrypoint.sh /
# ENTRYPOINT [ "sh","/entrypoint.sh" ]
 
# collect static files
RUN python manage.py collectstatic --noinput

RUN adduser -D user
RUN chown -R user:user .

USER user

