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

    def login(self, username="test_account", password="p@ssw0rd"):
        login = self.client.login(username=username, password=password)
        return login

    def test_login_successful(self):
        self.assertTrue(self.login())
        response = self.client.get('/my_details/')
        self.assertEqual(str(response.context['user']),"test_account")
        self.assertContains(response,"Test Account")

    def test_login_fail(self):
        self.assertFalse(self.login(username="test_account", password="123456789"))

    def test_loginpage_rendered_template(self):
        response = c.get('/accounts/login/')
        self.assertEqual (response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_mydetails_rendered_template(self):
        self.login()
        response = self.client.get('/my_details/')
        self.assertTemplateUsed(response, 'movie_store/customer_details.html')


class MoviesTest(TestCase):

    @classmethod
    def setUpTestData(cls):
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
        self.assertTrue(len(response.context['page_obj'])== 1)

    def test_movie_details(self):
        response = c.get('/movie_details/1/')
        self.assertContains(response, "Francis Ford Coppola")
        self.assertContains(response, 1972)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response, 'movie_store/movie_details.html')