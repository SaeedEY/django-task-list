FROM python:3.11
# FROM localhost:5000/python/python:3.9.12

ARG APP_PORT=8000

RUN mkdir /application
WORKDIR /application

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py makemigrations taskmodule
RUN python manage.py migrate

CMD python manage.py runserver $APP_PORT