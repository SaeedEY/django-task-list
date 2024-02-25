# Django TaskList API
A Serving application (web api) written in Django and simple database engine (Sqlite). 
below concepts are implemented:
- Subscriber (Custom User) 
- Bucket : in order to have a top level Container for Task
- Task : used in deep level 

##### Up coming Features
- DeleteTask / DeleteBucket
- Multi Subscriber Tasks / Multi Subscriber Buckets
- Multi Bucket Tasks
- Role Based Tasks / Role Based Buckets
- Subscriber Changes' History
- Bucket Changes' History / Task Changes' History

##### Current Features 
- EditTask / EditBucket <sup>new</sup>
- Register / Login / Authenticate / Logout
- CreateTask / CreateBucket

## Docs
You might better to visit the [Swagger Editor](https://editor.swagger.io/) and import our [openapi.json](https://raw.githubusercontent.com/SaeedEY/django-task-list/master/openapi.json) [latest version] to explore.

## Installation
To run this app you required to fulfill the below requirements:
- Python 3.9+
- ⤷ django
- ⤷ django-ninja


##### As ususal 
Following the [Django - The development server](https://docs.djangoproject.com/en/5.0/intro/tutorial01/#the-development-server) docs on serving the application, execute below domands in your end for test purpose :
```sh
git clone https://github.com/SaeedEY/django-task-list.git
cd django-task-list
python3 manage.py makemigrations taskmodule
python3 manage.py migrate
python3 manage.py runserver
```
##### Docker
In order to install 
```sh
git clone https://github.com/SaeedEY/django-task-list.git
cd django-task-list
docker-compose up --build
```

## Contribution
You are totally wellcome to handle the UI side on your own and dont forget to update this [README.md](https://github.com/SaeedEY/django-task-list/blob/master/README.md) and add your repo under the **Link** section.

## Links
-- REF1