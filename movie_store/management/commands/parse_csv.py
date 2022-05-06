import csv
import random
import decimal
#import re
#from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User
from faker import Faker
from movie_store.models import Director,Movie,Cart,Customer,LineItem,Order
import ast

class Command(BaseCommand):
    help = 'Load data from csv along with faker values into tables'
    
    def handle(self, *args, **options):
        Movie.objects.all().delete()
        Cart.objects.all().delete()
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
        Director.objects.all().delete()

        print("Tables dropped successfully")

        director_list = []
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        
        with open(f'{base_dir}/movie_store/data/movie_clean_big.csv', 'r') as file:
            csvfile = csv.reader(file, delimiter=";")
            next(csvfile)
            for count, line in enumerate(csvfile):
                print("Processing line",count+1)

                #director = re.findall("(?:\"|\')(.*?)(?:\"|\')",line[13])[0]
                try:
                    directors = line[13]
                    res = ast.literal_eval(directors)
                    director = res[0]
                    if director not in director_list:
                        director_list.append(director)
                        director_name = Director.objects.create(name=director)
                        director_name.save()
                except IntegrityError:
                    pass

                actors_str = line[9]
                res = ast.literal_eval(actors_str)
                actor = ""
                for count,i in enumerate(res):
                    if count == len(res)-1:
                        actor += i
                    else:
                        actor += f"{i}, "
                
                genres_str = line[10]
                res = ast.literal_eval(genres_str)
                genre = ""
                for count,i in enumerate(res):
                    if count == len(res)-1:
                        genre += i
                    else:
                        genre += f"{i}, "
                
                movie_name = Movie(
                    title = line[0],
                    rating = line[1],
                    year_released = int(line[2][0:4]),
                    imdb_rating = line[3],
                    imdb_votes = line[4],
                    actor=actor,
                    genre=genre,
                    metascore = int(line[5].split(".")[0]),
                    poster_link = line[6],
                    tagline = line[11],
                    director = Director.objects.get(name=director),
                    runtime = [int(word) for word in line[14].split() if word.isdigit()][0],
                    plot_summary = line[12],
                    imdb_link = line[15],
                    price = int(decimal.Decimal(random.randrange(155,899))/100),
                )
                movie_name.save()

        fake = Faker()

        for i in range(10):
            first_name = fake.first_name(),
            first_name = str(first_name[0])
            last_name = fake.last_name(),
            last_name = str(last_name[0])
            username = first_name + last_name,
            username = username[0]
            try:
                user = User.objects.create_user(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = fake.ascii_free_email(), 
                    password = 'p@ssw0rd')
                customer = Customer.objects.get(user = user)
                customer.address = fake.address(),
                customer.address = str(customer.address[0])
                customer.save()
            except IntegrityError:
                next

        products = list(Movie.objects.all())
        for i in range(10):
            random_id = random.randint(0,999)
            cart = Cart.objects.create(
                product = products[random_id],
                quantity = random.randrange(1,42),
            )
            cart.save()

        customers = Customer.objects.all()
        for customer in customers:  
            for i in range(3):
                order = Order.objects.create(
                customer = customer,
                )
                order.save()

        orders = Order.objects.all()
        carts = Cart.objects.all()
        for order in orders:
            for cart in carts:
                line_item = LineItem.objects.create(
                    quantity = cart.quantity,
                    product = cart.product,
                    cart = cart,
                    order = order,
                )
                line_item.save()
        
        print("CSV Parsing done")
