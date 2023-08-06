""" """
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time


def login_aza(headless=True):
    """ """
    url = "https://www.avanza.se"
    delay = 10

    # Init webdriver
    options = webdriver.ChromeOptions()
    options.headless = headless
    options.add_argument("--start-maximized")

    try:
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
    except Exception as e:
        print(e)
        gChromeOpts = webdriver.ChromeOptions()
        gChromeOpts.add_argument("window-size=19201480")
        gChromeOpts.add_argument("distable-dev-shm-usage")
        driver = webdriver.chrome(chrome_options=gChromeOpts,
                                  executable_path=ChromeDriverManager().install())

    # Open the website
    driver.get(url)

    xpath = '//span[text()="Logga in"]'
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                By.XPATH, xpath)))

    # Click login button
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", element)
    # Use the Bank-id

    xpath = '//span[text()="Mobilt BankID på annan enhet"]'
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", element)

    # Wait for bank id
    time.sleep(40)
    xpath = '//div[text()="Min ekonomi"]'
    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                By.XPATH, xpath)))

    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", element)

    xpath = '//a[@href="/min-ekonomi/innehav.html"]'
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", element)

    return driver
