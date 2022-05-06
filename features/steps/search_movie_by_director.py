import urllib
from urllib.parse import urljoin, urlparse
from behave import given, when, then
import time

@given(u'I navigate to the home page')
def step_impl(context):
    base_url = context.get_url()
    context.browser.get(base_url)

@given(u'I put the director\'s name in the search bar')
def step_impl(context):
    element = context.browser.find_element_by_class_name('search-bar')
    element.send_keys("Francis Ford Coppola")    

@given(u'I click radio button to search by director and submit')
def step_impl(context):
    element = context.browser.find_element_by_id('director')
    element.click()
    element.submit()

@when(u'I press the link to the director\'s page')
def step_impl(context):
    context.browser.find_element_by_partial_link_text("Francis Ford Coppola").click()

@then(u'I should see the correct movie title on the director\'s page')
def step_impl(context):
    assert "The Godfather" in context.browser.page_source
    