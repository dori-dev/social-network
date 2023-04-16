FROM hub.hamdocker.ir/library/python:alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_PASSWORD admin

RUN mkdir /app
RUN mkdir -p /app/logs
WORKDIR /app
ADD ./resolv.conf /etc/resolv.conf
RUN apk update
RUN apk add --no-cache build-base
ADD ./resolv.conf /etc/resolv.conf
RUN pip install --upgrade pip
ADD ./requirements /app/requirements
ADD ./requirements.txt /app
RUN pip install -r requirements.txt

CMD python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python manage.py createsuperuser --noinput --user admin --email admin@site.com; \
    gunicorn -b 0.0.0.0:8000 config.wsgi
