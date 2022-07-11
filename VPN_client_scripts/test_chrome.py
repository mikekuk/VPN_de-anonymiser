
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

options = Options()
options.add_argument("-profile")
options.add_argument("/home/user/.config/google-chrome/Profile 1")
# options.add_argument("--user-data-dir=chrome-data")

chrome_driver = "/home/user/chrome_driver/chromedriver"

driver = webdriver.Chrome(chrome_driver, options=options)

driver.get("http://www.uwe.ac.uk")
time.sleep(10)
driver.quit()

# Issues cause by bug in Chrome 103. More detilas at: https://github.com/SeleniumHQ/selenium/issues/10799