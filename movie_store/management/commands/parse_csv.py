import csv
import random
import decimal
import re
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User
from faker import Faker
from movie_store.models import Director,Actor,Genre,Movie,Cart,Customer,LineItem,Order

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
        Actor.objects.all().delete()
        Genre.objects.all().delete()

        print("Tables dropped successfully")

        director_list,artist_list,genre_list = [],[],[]
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        
        with open(f'{base_dir}/movie_store/data/movie_clean.csv', 'r') as file:
            csvfile = csv.reader(file, delimiter=";")
            next(csvfile)
            for count, line in enumerate(csvfile):
                print("line",count+1)

                director = re.findall("(?:\"|\')(.*?)(?:\"|\')",line[13])[0]
                print(director)
                if director not in director_list:
                    director_list.append(director)
                    director_name = Director.objects.create(name=director)
                    director_name.save()

                actor_line = re.findall("(?:\"|\')(.*?)(?:\"|\')",line[9])
                genre_line = re.findall("(?:\"|\')(.*?)(?:\"|\')",line[10])
                for i in range(4):
                    try:
                        if actor_line[i] not in artist_list:
                            artist_list.append(actor_line[i])
                            artist_name = Actor.objects.create(name=actor_line[i])
                            artist_name.save()
                    except IndexError:
                        break
                
                for i,num in enumerate(genre_line):
                    try:
                        if i < 4:
                            if genre_line[i] not in genre_list:
                                genre_list.append(genre_line[i])
                                genre_name = Genre.objects.create(genre=genre_line[i])
                                genre_name.save()
                        else:
                            break
                    except IndexError:
                        break

                movie_name = Movie(
                    title = line[0],
                    rating = line[1],
                    year_released = int(line[2][0:4]),
                    imdb_rating = line[3],
                    imdb_votes = line[4],
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

                for i in range(4):
                    try:
                        artist_add = Actor.objects.get(name=actor_line[i])
                        movie_name.actor.add(artist_add)
                    except IndexError:
                        break

                for i,num in enumerate(genre_line):
                    try:
                        if i < 4:
                            genre_add = Genre.objects.get(genre=genre_line[i])
                            movie_name.genre.add(genre_add)
                        else:
                            break
                    except IndexError:
                        break
                movie_name.save()

        fake = Faker()

        for i in range(10):
            first_name = fake.first_name(),
            first_name = str(first_name[0])
            last_name = fake.last_name(),
            last_name = str(last_name[0])
            username = first_name + last_name,
            username = username[0]
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
                """
                title = line[0]
                rating = line[1]
                year = line[2]
                imdb_rating = line[3]
                imdb_votes = line[4]
                metascore = line[5]
                poster_link = line[6]
                actors = line[9]
                genre = line[10]
                tagline = line[11]
                plot_summary = line[12]
                director = line[13]
                runtime = line[14]
                imdb_url = line[15]
                """