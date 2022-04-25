import csv
import random
import decimal
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from django.contrib.auth.models import User
from faker import Faker
from movie_store.models import Year_released,IMDB_rating,Director,Artist,Genre,Movies

class Command(BaseCommand):
    help = 'Load data from csv along with faker values into tables'
    
    def handle(self, *args, **options):
        Movies.objects.all().delete()
        Year_released.objects.all().delete()
        IMDB_rating.objects.all().delete()
        Director.objects.all().delete()
        Artist.objects.all().delete()
        Genre.objects.all().delete()

        print("Tables dropped successfully")

        year_list,imdb_list,director_list,artist_list,genre_list = [],[],[],[],[]
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
       
        with open(f'{base_dir}/movie_store/data/imdb_top_1000.csv', 'r') as file:
            csvfile = csv.reader(file, delimiter=",")
            next(csvfile)
            for count, line in enumerate(csvfile):
                print("line",count)
                year = line[2]
                if year not in year_list:
                    year_list.append(year)
                    year_released = Year_released.objects.create(year=year)
                    year_released.save()

                rating = line[6]
                if rating not in imdb_list:
                    imdb_list.append(rating)
                    imdb_rating = IMDB_rating.objects.create(rating=rating)
                    imdb_rating.save()

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
                    year_released = Year_released.objects.get(year=year),
                    imdb_rating = IMDB_rating.objects.get(rating=rating),
                    director = Director.objects.get(name=director),
                    runtime = [int(word) for word in line[4].split() if word.isdigit()][0],
                    certificate = line[3],
                    plot_summary = line[7],
                    poster_link = line[0],
                    gross = line[15]
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