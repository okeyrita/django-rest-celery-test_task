# Specsharing Python Developer Test Task

## Description

Implement __Django + Django Rest framework backend__ with the following conditions:

* User authorization

* Wallets with 3 currencies: rubles, euro, dollars

* Replenishment and withdrawal of money from wallets

* Converting money between wallets

* Transferring money between users

* Daily __celery__ task to synchronize currencies with an online service. (ex. [link](https://www.cbr-xml-daily.ru/daily.xml​))

## Content of the project

* Django project `test_task`

* App `wallet`

* Initial description of the task `Тестовое задание для backend.pdf`

## Implementation

#### Web paths

* `admin/` - admin panel

* `accounts/login/` - authorization panel

* `wallet/` - wallet data of user

* `convert/` - convert page
    * Converting money between wallets

* `transfer/` - transfer money page
    * Transferring money between users

* `topup/` - top up money page

* `withdraw/` - withdraw money page

#### Admin panel 

* _login_: admin
_password_: admin

#### Test users

1. _login_: Anna 
_password_: LuckySmile

2. _login_: Masha 
_password_: LuckySmile

#### Database

Used default Django database __sqlite3__

## How to run 

#### How run locally on your laptop

* Save project 
```
git clone https://github.com/okeyrita/django-rest-celery-test_task.git
```
* Go to main directory
```
cd 
```
* Start a local web server
```
python3 manage.py runserver
```
* Go to web browser and go to web page
```
http://localhost:8000/login
```
* To stop the local web server press `Ctrl+C`
