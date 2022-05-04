import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then
import time

@given(u'I navigate to the movie list page')
def step_impl(context):
    base_url = context.get_url()
    open_url = urljoin(base_url, '/movies/')
    context.browser.get(open_url)


@when(u'I choose a movie and click on it')
def step_impl(context):
    context.browser.find_element_by_partial_link_text('10 THINGS I HATE ABOUT YOU').click()


@when(u'I click on add to basket')
def step_impl(context):
    context.browser.find_element_by_class_name('button2').click()


@then(u'I should see the movie title on the cart page')
def step_impl(context):
    context.browser.find_element_by_partial_link_text('Cart').click()
    assert '10 Things I Hate About You' in context.browser.page_source
    