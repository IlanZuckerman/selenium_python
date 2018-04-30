import os, logging
import pytest
import time
from time import gmtime, strftime
from base.webdriverfactory import WebDriverFactory
import utilities.custom_logger as cl
from traceback import print_stack

log = cl.customLogger(logging.DEBUG)

report_path = None  # initialized during run time

# @pytest.yield_fixture()
# def setUp():
#     print("Running method level setUp")
#     yield
#     print("Running method level tearDown")


@pytest.yield_fixture(scope="class")
def oneTimeSetUp(request, username, password, browser, engineUrl):
    print("Running one time setUp")
    wdf = WebDriverFactory(username, password, browser, engineUrl)
    driver = wdf.getWebDriverInstance()

    if request.cls is not None:
        request.cls.driver = driver

    yield driver
    # this would be done as teardown (after yield)
    driver.quit()
    print("Running one time tearDown")

def pytest_addoption(parser):
    parser.addoption("--username", help="Username for logging in")
    parser.addoption("--password", help="Password for logging in")
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")
    parser.addoption("--engineUrl", help="URL for engine. for example https://b01-h21-r620.rhev.openstack.engineering.redhat.com")

@pytest.fixture(scope="session")
def username(request):
    return request.config.getoption("--username")

@pytest.fixture(scope="session")
def password(request):
    return request.config.getoption("--password")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")

@pytest.fixture(scope="session")
def engineUrl(request):
    return request.config.getoption("--engineUrl")


@pytest.fixture(scope="session")
def exec_report_path():
    global report_path
    full_path = ""

    fileName = 'exec_report_' + str(round(time.time() * 1000)) + '.csv'
    timeMeasureDir = '../time_measurements/'
    relativeFileName = timeMeasureDir + fileName.replace(" ", "")
    currentDirectory = os.path.dirname(__file__)
    destinationFile = os.path.join(currentDirectory, relativeFileName)
    destinationDirectory = os.path.join(currentDirectory, timeMeasureDir)

    try:
        if not os.path.exists((destinationDirectory)):
            os.makedirs(destinationDirectory)

        with open(destinationFile, 'w') as full_path:
            title = 'Execution report for RHEV build:,\n'
            date_time = 'Date:,' + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + '\n\n'
            table_titles = 'Test name,Duration in seconds'
            full_path.writelines([title, date_time, table_titles])

        log.info('Execution report created in directory: ' + destinationFile)
    except:
        log.error('### Exception Occurred while creating exec report')
        print_stack()

    report_path = full_path
