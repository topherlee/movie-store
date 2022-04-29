import csv
import random
import decimal
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User
from faker import Faker
from movie_store.models import Director,Artist,Genre,Movies,Cart,Customer,LineItem,Order

class Command(BaseCommand):
    help = 'Load data from csv along with faker values into tables'
    
    def handle(self, *args, **options):
        Movies.objects.all().delete()
        Cart.objects.all().delete()
        LineItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        User.objects.all().delete()
        Director.objects.all().delete()
        Artist.objects.all().delete()
        Genre.objects.all().delete()

        print("Tables dropped successfully")

        director_list,artist_list,genre_list = [],[],[]
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        
        with open(f'{base_dir}/movie_store/data/imdb_top_1000.csv', 'r') as file:
            csvfile = csv.reader(file, delimiter=",")
            next(csvfile)
            for count, line in enumerate(csvfile):
                print("line",count)

                director = line[9]
                if director not in director_list:
                    director_list.append(director)
                    director_name = Director.objects.create(name=director)
                    director_name.save()

                for i in range(10,14):
                    if line[i] not in artist_list:
                        artist_list.append(line[i])
                        artist_name = Artist.objects.create(name=line[i])
                        artist_name.save()

                genre = line[5].split(",")
                for i in genre:
                    if i not in genre_list:
                        genre_list.append(i)
                        genre_name = Genre.objects.create(genre=i)
                        genre_name.save()

                movie = line[1]
                movie_name = Movies(
                    title = movie,
                    year_released = line[2],
                    imdb_rating = line[6],
                    director = Director.objects.get(name=director),
                    runtime = [int(word) for word in line[4].split() if word.isdigit()][0],
                    certificate = line[3],
                    plot_summary = line[7],
                    poster_link = line[0],
                    gross = line[15],
                    price = int(decimal.Decimal(random.randrange(155,899))/100),
                )
                movie_name.save()

                artist1= Artist.objects.get(name=line[10])
                artist2= Artist.objects.get(name=line[11])
                artist3= Artist.objects.get(name=line[12])
                artist4= Artist.objects.get(name=line[13])
                movie_name.artist.add(artist1,artist2,artist3,artist4)
                
                for i in genre:
                    movie_name.genre.add(Genre.objects.get(genre=i))

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

        products = list(Movies.objects.all())
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
                poster_link = line[0]
                title = line[1]
                year = line[2]
                certificate = line[3]
                runtime = line[4]
                genre = line[5]
                rating = line[6]
                plot_summary = line[7]
                director = line[9]
                """