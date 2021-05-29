#ON HOLD DUE TO WORK ON MY BACHELOR'S DEGREE PROJECT


# Shop ordering system
Shop management system created with Django.

## Table of contents
* [Info](#general-info)
* [TODO](#todo)
* [Technologies](#technologies)
* [Setup](#setup)
## General info 
Project is general shop management system. It allows user to create orders, allowing to choose which products should be ordered, and how many of them, while removing necessary ingredients from stock, and blocking user if there in no enough of them in stock. It allows to print timed reports where transactions are summed up to show profit of given timeframe.

## TODO
* Extend Employee management
* Positions
* Support employee position and permissions
* Remaking product recipe in order
* Expand app to be RESTful
* Visual upgrade
* Preparation checklist for Employees 
* Extend info in reports

## Technologies
* Python 3.9.1
* Django
* Venv
* Bootstrap 4.5

## Setup
 Install Django, create superuser and run app
```
cd ../Shop_ordering_system
python manage.py createsuperuser
python manage.py runserver
```
move to localhost:8000/admin and create employee connected with superuser  
then move to localhost:8000/ordersys/orders/ and log in.

