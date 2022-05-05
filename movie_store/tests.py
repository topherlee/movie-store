from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Movie, Director, Customer
c=Client()

class LoginPageTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username="test_account",
            first_name="Test",
            last_name="Account",
            email="test@123.com",
        )
        user.set_password('p@ssw0rd')
        user.save()
        Customer.objects.filter(user_id=1).update(address="Nesselweg 45, Cologne 51109, Germany")

    def test_login(self):
        login = self.client.login(username="test_account", password="p@ssw0rd")
        self.assertTrue(login)

    def test_rendered_template(self):
        response = c.get('/accounts/login/')
        self.assertEqual (response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')


class MoviesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        Director.objects.create(name="Francis Ford Coppola").save()
        Movie.objects.create(
            title="The Godfather",
            rating="R",
            year_released=1972,
            imdb_rating=9.2,
            imdb_votes="1,552,849",
            actor="Marlon Brando, Al Pacino, James Caan, Richard S. Castellano, Robert Duvall, Sterling Hayden, John Marley, Richard Conte, Al Lettieri, Diane Keaton, Abe Vigoda, Talia Shire, Gianni Russo, John Cazale, Rudy Bond",
            genre="Crime, Drama",
            metascore=100,
            poster_link="https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY268_CR3,0,182,268_AL__QL50.jpg",
            tagline="An offer you can't refuse",
            director=Director.objects.get(name="Francis Ford Coppola"),
            runtime=175,
            plot_summary="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
            imdb_link="https://www.imdb.com/title/tt0068646/",
            price=1.0
        ).save()

    def test_movie_list(self):
        response = c.get('/movies/')
        self.assertContains(response, "The Godfather")
        self.assertTemplateUsed(response, 'movie_store/movie_list.html')
        self.assertEqual(response.status_code,200)

    def test_movie_details(self):
        response = c.get('/movie_details/1/')
        self.assertContains(response, "Francis Ford Coppola")
        self.assertContains(response, 1972)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'movie_store/movie_details.html')