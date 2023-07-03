# skateZstore-Ecommerce
## INTRO
This is an Ecommerce Project of skateboard products.
I have included an admin page on top of the website inorder to add new products and product offers and stocks.
I have build the front end using bootstrap,html,css,js.
I have build the back end using django's Framework.
I have incorporated Postgresql as database for user and product information.
Also i have hosted this website in AWS using cloudflare by purchasing domain from freenom.com
## Pre-requesites:
- Python 3.8
- pip3
- postgreSQL 12
- **Note:** It is advised to use virtual environment to run your application!
  - Install venv
    - ```bash
        sudo apt install python3.8-venv
      ```
 ## Installation:
  - Create virtual environment
    - ```bash
      python3.8 -m venv “name of environment”
      ```
  - connect to the virtual environment
    - ```bash
      source name_of_environment/bin/activate
      ```
  - Clone this repository
  - Install the requirements.txt file
    - ```bash
      pip install -r requirements.txt
      ```
  - Create a database in postgres.
  - Create a .env file inside the folder containing settings.py.
  - **Things to add in settings.py:**
    - Database credentials.
    - Get the ACCOUNT SID and ACCOUNT_SECURITY_API_KEY from twilio website.
    - Django secret key from any secret key generator.
  - Migrate the models created onto database.
    - ```bash
      python manage.py makemigrations
      ```
    - ```bash
      python manage.py migrate
      ```
  - Run the application on djangos default port 8000
    - ```bash
      python manage.py runserver
      ```
## Links

* [Web site](https://www.skatezstore.tk)
* [Source code](https://github.com/fayasPA/skateZstore-Ecommerce)
