FROM python:3.11

ARG APP_PORT_ARG
ENV APP_PORT=${APP_PORT_ARG:-8888}

RUN mkdir /application
WORKDIR /application

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py makemigrations taskmodule
RUN python manage.py migrate

EXPOSE $APP_PORT

#CMD python manage.py runserver $APP_PORT
CMD echo $APP_PORT