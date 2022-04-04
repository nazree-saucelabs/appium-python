import pytest
from os import environ

from appium import webdriver


import urllib3
urllib3.disable_warnings()


def pytest_addoption(parser):
    parser.addoption("--dc", action="store", default='us', help="Set Sauce Labs Data Center (US or EU)")


@pytest.fixture
def data_center(request):
    return request.config.getoption('--dc')


@pytest.fixture
def android_driver(request, data_center):

    username_cap = environ['SAUCE_USERNAME']
    access_key_cap = environ['SAUCE_ACCESS_KEY']
    
    caps = {
        'sauce:options': {
            'username': username_cap,
            'accessKey': access_key_cap,
        },
        'appium:deviceName': 'Google Pixel 4 XL GoogleAPI Emulator',
        'platformName': 'Android',
        'appium:platformVersion': '11.0',
        'name': request.node.name,
        'app': "https://github.com/saucelabs/sample-app-mobile/releases/download/2.7.1/Android.SauceLabs.Mobile.Sample.app.2.7.1.apk"
    }

    if data_center and data_center.lower() == 'eu':
        sauce_url = 'http://ondemand.eu-central-1.saucelabs.com/wd/hub'
    else:
        sauce_url = 'http://ondemand.us-west-1.saucelabs.com/wd/hub'

    driver = webdriver.Remote(sauce_url, desired_capabilities=caps)
    yield driver
    sauce_result = "failed" if request.node.rep_call.failed else "passed"
    driver.execute_script("sauce:job-result={}".format(sauce_result))
    driver.quit()

@pytest.fixture
def ios_driver(request, data_center):

    username_cap = environ['SAUCE_USERNAME']
    access_key_cap = environ['SAUCE_ACCESS_KEY']
   
    caps = {
        'username': username_cap,
        'accessKey': access_key_cap,
        'appium:deviceName': 'iPhone 12 Pro Max Simulator',
        'platformName': 'iOS',
        'appium:platformVersion': '14.5',
        'name': request.node.name,
        'app': 'https://github.com/saucelabs/sample-app-mobile/releases/download/2.7.1/iOS.RealDevice.SauceLabs.Mobile.Sample.app.2.7.1.ipa'
    }

    if data_center and data_center.lower() == 'eu':
        sauce_url = "http://ondemand.eu-central-1.saucelabs.com/wd/hub"
    else:   
        sauce_url = "http://ondemand.us-west-1.saucelabs.com/wd/hub"

    driver = webdriver.Remote(sauce_url, desired_capabilities=caps)
    yield driver
    sauce_result = "failed" if request.node.rep_call.failed else "passed"
    driver.execute_script("sauce:job-result={}".format(sauce_result))
    driver.quit()

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # this sets the result as a test attribute for Sauce Labs reporting.
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set an report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "rep_" + rep.when, rep)

