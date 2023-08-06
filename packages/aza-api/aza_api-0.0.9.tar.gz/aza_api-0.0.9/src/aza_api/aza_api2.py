""" """
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime
from aza_api.html_to_df import html_to_df

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

class aza_api2():

    def __init__(self):
        pass

    def login(self, headless=False):
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
        time.sleep(1)

        xpath = '//span[text()="Logga in"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        xpath = '//span[text()="Mobilt BankID på annan enhet"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        # Wait for bank id
        xpath = '//div[text()="Min ekonomi"]'
        elem = WebDriverWait(driver, 100).until(EC.presence_of_element_located((
                                                By.XPATH, xpath)))

        self.driver = driver

        return driver

    def fetch_portfolio(self):
        driver = self.driver
        delay = 10
        xpath = '//div[text()="Min ekonomi"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        time.sleep(1)
        xpath = '//a[@href="/min-ekonomi/innehav.html"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        driver.execute_script("arguments[0].click();", elem)

        xpath = '//h4[@data-e2e="total-values-desktop-total-value"]'
        elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((
                                                  By.XPATH, xpath)))
        self.tot_val = float(elem.text.replace("kr", "").replace(" ", "").strip())

        time.sleep(1)
        df = html_to_df(driver.page_source)
        self.df = df
        self.port_val = self.df[df.columns[4]].sum()
        self.cash_val = self.tot_val - self.port_val

        self.portfolios = {"all": df}
        print(f"Fetched self.portfolios: {self.portfolios.keys()}")

        return df

    def login_and_fetch(self, headless=False):
        """Convenience function"""
        self.login(headless=headless)
        self.fetch_portfolio()

    def save_csv(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_aza_{today}.csv"
        self.df.to_csv(filename)

    def save_ascii(self):
        """ """
        today = datetime.now().strftime("%Y%m%d")
        filename = f"portfolio_aza_{today}"
        with open(f'./{filename}.txt', 'w') as fo:
            fo.write(self.df.__repr__())
