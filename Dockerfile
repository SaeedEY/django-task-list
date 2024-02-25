FROM python:3.11

ARG APP_PORT=8888

RUN mkdir /application
WORKDIR /application

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py makemigrations taskmodule
RUN python manage.py migrate

CMD python manage.py runserver $APP_PORT