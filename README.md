# Project Title

This is a selenium webDriver effort made for Functional UI E2E tests when the system is scaled. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites
This is a list of working components for this test suit to run. The versions are from when the code was written, meaning
that later versions could also work but not necessarily.

Python -> 3+

Selenium -> 3.9.0

Java -> 8+

Gecko Driver -> 0.19.1  you can download it here: https://github.com/mozilla/geckodriver/releases

FireFox -> 57.0.1 


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

Navigate to projects Root and execute command with this pattern:

py.test -s -v tests/home/test_login.py --browser=firefox --engineUrl=<url> --username=<...> --password=<...> --html=report.html --self-contained-html

Example:
```
py.test -s -v tests/home/test_login.py --browser=firefox --engineUrl=https://b01-h21-r620.rhev.openstack.engineering.redhat.com --username=moshe --password=123 --html=report.html --self-contained-html
```

### Tests After run artifacts

Log:
tests/home/automation.log

Screenshots upon failure:
screenshot

Detailed Test Suit report:
tests/home/report.html

### Break down into end to end tests

####test_invalid_login
####test_valid_login
####test_create_L1vm_from_template
####test_start_previosly_created_L1_vm
####test_reboot_bulk_of_20_L1_vms
####test_create_L2vm_from_template
####test_start_previosly_created_L2_vm
####test_create_nested_host_and_check_status
####test_putting_bulk_of_nested_hosts_to_maintenance

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```