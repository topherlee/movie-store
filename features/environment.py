import os, urllib
import django
from django.shortcuts import resolve_url
from django.test import selenium
from django.test.testcases import TestCase
from django.test.runner import DiscoverRunner
from django.test.testcases import LiveServerTestCase
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.contrib.auth.models import User
from django.db import connections
#from selenium.webdriver.firefox.options import Options 


os.environ["DJANGO_SETTINGS_MODULE"] = "store_project.settings"
django.setup()
CHROME_DRIVER = os.path.join('driver/chromedriver')
DRIVER_PATH = os.path.join(os.path.join(os.path.dirname(__file__), 'driver'), 'chromedriver')
options = Options()

def before_all(context):
    #context.browser = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER)
    context.browser = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    context.browser.set_page_load_timeout(time_to_wait=200)

def before_scenario(context, scenario):
    context.test = TestCase()
    context.test.setUpClass()
"""
def after_scenario(context, scenario):
    #context.test.tearDownClass()
    del context.test
"""

def after_feature(context, feature):
    if feature.name == "signup":
        conn = connections['default']
        conn.connect()
        if User.objects.last().username == "test_account":
            User.objects.get(username="test_account").delete()
        conn.close()

def after_all(context):
    context.browser.quit()
