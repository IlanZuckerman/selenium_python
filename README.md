# Project Title

This is a selenium webDriver effort made for Functional UI E2E tests when the system is scaled. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Python -> 3+
Selenium -> 3.9.0
Java -> 8+
Gecko Driver -> 0.19.1  you can download it here: https://github.com/mozilla/geckodriver/releases
```
Give examples
```

### Installing
**Gecko Driver:**
Download latest	geckodriver	from this location:
https://github.com/mozilla/geckodriver/releases
Extract	the	geckodriver	and	save	the	geckodriver	at	/usr/local/bin/
chmod +x /usr/local/bin/geckodriver

**Selenium Webdriver:**
pip3 install selenium==3.9.0

**If you dont have pip installed:**
https://www.tecmint.com/install-pip-in-linux/

**Cloning the project to your machine:**
https://github.com/maximum71/selenium_python.git

**Installing pip packages**
From Projects root:
pip install -r requirements.txt


## Running the tests

Inside tests/home/test_login.py search for a line with self.lp.login('', '') and insert in place of empty quotes relevant
user name and password.
Example:
```
self.lp.login('moshe', '123')
```
Navigate to projects Root and execute command with this pattern:
py.test -s -v tests/home/test_login.py --browser=firefox --engineUrl=<url> --html=report.html --self-contained-html
Example:
```
py.test -s -v tests/home/test_login.py --browser=firefox --engineUrl=https://b01-h21-r620.rhev.openstack.engineering.redhat.com --html=report.html --self-contained-html
```

### Tests After run artifacts

Log:
tests/home/automation.log

Screenshots upon failure:
screenshot

Detailed Test Suit report:
tests/home/report.html

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```