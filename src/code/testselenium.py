from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def run():
    options = Options()
    #options.add_argument("--disable-notifications")
    options.add_argument("headless")

    driver_location = "/usr/bin/chromedriver"
    binary_location = "/usr/bin/google-chrome"

    option = webdriver.ChromeOptions()
    options.binary_location = binary_location

    driver = webdriver.Chrome(executable_path=driver_location, chrome_options=options)
    driver.get("https://www.google.com/")
    driver.close()
    return "ok"

