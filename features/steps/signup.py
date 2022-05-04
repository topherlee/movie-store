import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then
import time


@given(u'I click on sign up')
def step_impl(context):
    element = context.browser.find_element_by_link_text("Sign Up")
    element.click()


@when(u'I enter my details and submit')
def step_impl(context):
    context.browser.find_element_by_name("username").send_keys("test_account")
    context.browser.find_element_by_name("first_name").send_keys("John")
    context.browser.find_element_by_name("last_name").send_keys("Doe")
    context.browser.find_element_by_name("password1").send_keys("p@ssw0rd5")
    context.browser.find_element_by_name("password2").send_keys("p@ssw0rd5")
    context.browser.find_element_by_name("email").send_keys("test_account@gmail.com")
    context.browser.find_element_by_name("address").send_keys("North Square, Aberdeen AB11 5DX, United Kingdom")
    context.browser.find_element_by_name("Sign Up").click()
    time.sleep(3)


@then(u'I should be registered and logged in on the homepage')
def step_impl(context):
    print(context.get_url())
    assert "Logout (test_account)" in context.browser.page_source