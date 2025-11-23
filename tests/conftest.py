import os
import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions


# Load BrowserStack credentials from env vars
BROWSERSTACK_USERNAME = os.getenv("BROWSERSTACK_USERNAME")
BROWSERSTACK_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")


if not BROWSERSTACK_USERNAME or not BROWSERSTACK_ACCESS_KEY:
   raise Exception("❌ Missing BrowserStack credentials in environment variables.")




def get_caps(env):
   if env == "win_chrome":
       return {
           "browserName": "Chrome",
           "browserVersion": "latest",
           "bstack:options": {
               "os": "Windows",
               "osVersion": "10",
               "sessionName": "Windows Chrome",
               "buildName": "browserstack-demo",
           },
       }
   elif env == "mac_firefox":
       return {
           "browserName": "Firefox",
           "browserVersion": "latest",
           "bstack:options": {
               "os": "OS X",
               "osVersion": "Ventura",
               "sessionName": "Mac Firefox",
               "buildName": "browserstack-demo",
           },
       }
   elif env == "android_s22":
       return {
           "browserName": "Chrome",
           "bstack:options": {
               "deviceName": "Samsung Galaxy S22",
               "realMobile": True,
               "osVersion": "12.0",
               "sessionName": "Android S22",
               "buildName": "browserstack-demo",
           },
       }




@pytest.fixture(params=["win_chrome", "mac_firefox", "android_s22"])
def driver(request):
   env = request.param
   caps = get_caps(env)


   hub_url = (
       f"https://{BROWSERSTACK_USERNAME}:{BROWSERSTACK_ACCESS_KEY}"
       "@hub-cloud.browserstack.com/wd/hub"
   )


   options = FirefoxOptions() if env == "mac_firefox" else ChromeOptions()


   for k, v in caps.items():
       options.set_capability(k, v)


   driver = webdriver.Remote(command_executor=hub_url, options=options)


   yield driver
   driver.quit()




