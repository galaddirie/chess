# chess

A real-time multiplayer chess game web application built with Django and Django Channels

![image](https://user-images.githubusercontent.com/70884733/152384690-2f179f4b-128c-460e-a8e2-b16828948d6f.png)

## How to Install Repo

To install this repository on your machine
1. Clone this repository: `$ git clone https://github.com/galaddirie/chess.git` 
2. Create a virtual environment: `$ python3 -m venv venv`
3. activate virtual environment: `$ source venv/bin/activate`
4. navigate to the repository and install all the dependencies in requirements.txt: `$ pip install -r requirements.txt`
5. Create a new PostgreSQL database
    ```
    $ psql postgres
    $ CREATE DATABASE databasename
    $ \connect databasename
    ```
 6. Populate environment variables
 7. make migrations 
    ```
    $ python manage.py makemigrations 
    $ python manage.py migrate
    ```
  8. Run the application: `$ python manage.py runserver`
