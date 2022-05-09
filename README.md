# movie-store
# <a href = "http://store-movies.herokuapp.com">LINK TO LIVE VERSION</a>
A Django e-commerce website by Christopher Lee (52105866)

# Installation
### IMPORTANT: <br> To run behave test use this command: ```python manage.py behave --use-existing-database```
### Prerequisites:  
Create and activate a virtual environment:<br>
```
$ python -m venv .venv
$ source .venv/bin/activate
```
Then, install the dependencies before running the server:<br>
```
$ pip install -r requirements.txt
```
Finally, run the server:<br>
```
$ python manage.py runserver
```

# Features
<b>Guest (unregistered user)</b>:
Login / Sign up.
Search for movies by title, genre, or director name.
Browse movies sorting by title, IMDb rating, release year, or price.
Pick a random movie title.
Show movie details, link to IMDb page, and movie trailer.
Read reviews of each movie.
Select the amount and adding multiple movies to basket.
Update quantity or remove movie from the basket.

<b>Registered user</b>:
All features of the unregistered user plus:
Leave review for movies.
Basket checkout and place an order.
Show my details and my shipping address on a map.
Show my orders and list of items in the order.
View and edit my details (first name, last name, email address, shipping address).

<b>Admin</b>:
All features above plus:
View all registered customers’ details.
View all orders placed.
Add and modify details of a movie.

# How the app is developed
The app is developed by using Django framework and deployed to Heroku. PostgreSQL is used for the database of Heroku version while SQLite3 is used for the database of local version. Testing is done using Behave (behave-django) along with Selenium and Django built-in TestCase.

# Technical Details
Framework: Django 
Database: PostgreSQL (Heroku) and SQLite3 (local)<br>
Tables: 7 Tables<br>
Number of movies: 4500 titles<br>
Testing: Behave (behave-django, Selenium), Django TestCase<br>
Maps: Google Maps<br>
Dataset Source: <a href="https://www.kaggle.com/datasets/gorochu/complete-imdb-movies-dataset">Kaggle</a>
