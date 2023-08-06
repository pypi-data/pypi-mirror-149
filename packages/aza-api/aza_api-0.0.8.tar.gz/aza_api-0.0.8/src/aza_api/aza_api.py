"""Function to get fundamentals from Avanza."""
from requests_html import HTMLSession
from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
import nest_asyncio
import pandas as pd
import requests
import numpy as np
import re
from selenium import webdriver
from aza_api.map_aza_stock_to_url import map_aza_stock_to_url
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def get_aza_fundamentals(stock_tic):
    """HTML parser to get stock fundamentals from Avanza.

    :param stock_tic: E.g. "SKA-B.ST"
    """
    # Parse "om-aktien.html"
    stock_url = map_aza_stock_to_url(stock_tic, site='om-aktien.html')

    #chrome_options = Options(
    driver_path = r"lib/chrome_drivers/93_0_4577_63/chromedriver"
    options = webdriver.ChromeOptions()
    options.headless = True
    #driver = webdriver.Chrome(driver_path, chrome_options=options)
    try:
        s = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=s, options=options)
    except Exception as e:
        print(e)
        print("Failed to load Chromedriver install, trying 2nd option..")
        gChromeOptions = webdriver.ChromeOptions()
        gChromeOptions.add_argument("window-size=1920x1480")
        gChromeOptions.add_argument("disable-dev-shm-usage")
        driver = webdriver.Chrome(chrome_options=gChromeOptions,
                                  executable_path=ChromeDriverManager().install())
        # Try heroku
        print("Did second thing work?")

    try:
        import time
        time.sleep(2)
        driver.get(stock_url)
        time.sleep(2)
        print("Sucessfully got stock page")
    except Exception as e:
        print(stock_url)
        print(e)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)

    try:
        kort_namn = soup.find('aza-pair-list-key', string='Kortnamn')
        kort_namn = kort_namn.find_next_sibling().find_next_sibling().string
    except Exception as e:
        print(e, stock_tic, "Kortnamn")
        kort_namn = 0

    # Dividend_yield
    try:
        dividend_yield = soup.find('aza-pair-list-key', string='Direktavkastning')
        dividend_yield = dividend_yield.find_next_sibling().find_next_sibling().string
        dividend_yield = float(dividend_yield.replace(',', '.').replace("%", ""))*0.01
    except Exception as e:
        print(e, stock_tic, "Direktavkastning")
        dividend_yield = 0

    # PE-ratio
    try:
        pe_ratio = soup.find('aza-pair-list-key', string='P/E-tal')
        pe_ratio = pe_ratio.find_next_sibling().find_next_sibling().string
        pe_ratio = float(pe_ratio.replace(',', '.'))
    except Exception as e:
        print(e, stock_tic, "PE")
        pe_ratio = 0

    # Price/Book, Kurs/Eget kapital
    try:
        price_book = soup.find(
            'dt', string='Kurs/eget kapital ').find_next_sibling('dd').string
        price_book = float(price_book.replace(',', '.'))
    except Exception as e:
        print(e, stock_tic, "KURS/EGET KAP")
        price_book = 0

    # EPS
    try:
        eps_sek = soup.find('aza-responsive-overlay-button', header='Vinst/Aktie')
        eps_sek = eps_sek.find("span", {"class": "value"}).string
        eps_sek = eps_sek.replace(',', '.')
        eps_sek = float(eps_sek.replace('SEK', ''))
    except Exception as e:
        print(e, stock_tic, "VINST/AKTIE")
        eps_sek = "0"

    # Börsvärde (market cap)
    try:
        market_cap = soup.find('aza-pair-list-key', string=re.compile('Börsvärde'))
        market_cap = market_cap.find_next_sibling().find_next_sibling().string
        market_cap = market_cap.replace(',', '.')
        market_cap = market_cap.replace("\xa0", "")
        market_cap = market_cap.replace("MSEK","")
        market_cap = float(market_cap)*1e6
    except Exception as e:
        print(e, stock_tic, "BÖRSVÄRDE")
        market_cap = 0

    # Antal aktier
    try:
        antal_aktier = soup.find('aza-pair-list-key', string='Antal aktier')
        antal_aktier = antal_aktier.find_next_sibling().find_next_sibling().string
        antal_aktier = float(market_cap)
    except Exception as e:
        print(e, stock_tic, "Antal aktier")
        antal_aktier = 0

    # Senast betalt
    try:
        latest = soup.find('span', {"class": "latest"}).string
        latest = latest.replace("SEK", "").replace(",", ".")
        latest = float(latest)
    except Exception as e:
        print(e, stock_tic, "Senast betalt")
        latest = 0

    # Parse "om-bolaget.html"
    stock_url = map_aza_stock_to_url(stock_tic, site='om-bolaget.html')
    r = requests.get(stock_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # dividend/earnings
    try:
        dividend_earnings = soup.find(
            'dt', string='Andel utdelad vinst %').find_next_sibling('dd').string
        dividend_earnings = float(dividend_earnings.replace(',', '.'))*0.01
    except Exception:
        dividend_earnings = np.nan

    # Långfristiga skulder
    try:
        long_liabilities = soup.find(
            'td', string='Långfristiga skulder').find_next_sibling('td').string
        long_liabilities = float(long_liabilities.replace(u'\xa0', ''))
    except Exception:
        long_liabilities = 0
    # Kortfristiga skulder
    try:
        short_liabilities = soup.find(
            'td', string='Kortfristiga skulder').find_next_sibling('td').string
        short_liabilities = float(short_liabilities.replace(u'\xa0', ''))
    except Exception:
        short_liabilities = 0
    # Omsättningstillgångar
    try:
        current_assets = soup.find(
            'td', string='Summa omsättningstillgångar').find_next_sibling('td').string
        current_assets = float(current_assets.replace(u'\xa0', ''))
    except Exception:
        current_assets = 0
    # Kassa och bank
    try:
        cash_assets = soup.find(
            'td', string='Kassa och bank').find_next_sibling('td').string
        cash_assets = float(cash_assets.replace(u'\xa0', ''))
    except Exception:
        cash_assets = 0

    # NCAVPS net current assets value per share
    try:
        ncavps = (current_assets-(long_liabilities+short_liabilities))/antal_aktier
    except Exception as e:
        print(e, stock_tic, "ncavps")
        ncavps = 0

    # net cash
    try:
        net_cash_ps = (cash_assets-(long_liabilities+short_liabilities))/antal_aktier
    except Exception as e:
        print(e, stock_tic, "net_cash_ps")
        net_cash_ps = 0

    # Add to dataframe
    d = {'kortnamn': stock_tic,
         'dividend_yield': dividend_yield,
         'antal_aktier': antal_aktier,
         'pe_ratio': pe_ratio,
         'eps': eps_sek,
         'market_cap': market_cap,
         'dividend/earnings': dividend_earnings,
         'ncavps': ncavps,
         'net_cash_ps': net_cash_ps,
         'price_book': price_book,
         'latest': latest}

    df = pd.DataFrame(data=d, index=[0])

    return df
