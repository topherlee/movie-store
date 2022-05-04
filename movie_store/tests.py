from django.test import TestCase, Client
from django.contrib import auth
#from .models import Movie
c=Client()

class LoginPageTest(TestCase):
           
    def test_rendered_template(self):
        response = c.post('/accounts/login/', {'username':'','password':''})
        self.assertEqual (response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
