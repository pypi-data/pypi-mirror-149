# aza_api
Api to fetch data from Avanza website.

Package use chromedriver in order to render the Javascript from the page.

Idea for the user:
Incorporate this package in a webapp with a REST api.
The data may then be fetched fully in Google slides.

# Requirements

# Installation

Pip
```
pip install aza_api  # Installing
pip install aza_api -U  # Upgrading already installed package
```

Conda
```
conda install -c aza_api
```

# Usage

The `get_aza_fundamentals` method returns a pandas row.
Thus, it is easy to just append multiple stocks (tickers) to create a convenient dataframe.

```
from aza_api.aza_api import get_aza_fundamentals
df = get_aza_fundamentals("CAST.ST")  # Castellum

print(df.T)

>>>

                               0
kortnamn                 CAST.ST
dividend_yield            0.0284
antal_aktier       84012900000.0
pe_ratio                    8.29
eps                         29.3
market_cap         84012900000.0
dividend/earnings            NaN
ncavps                       0.0
net_cash_ps                  0.0
price_book                     0
latest                     244.6
```

# Development

While in root of this project. 
```
pip install -e .
```
This will install the package in editable mode.


# Testing

```
pytest tests/ -s
```

# Push project to Pip (PyPi) and Conda

### PyPi

https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56

Run in root
``` 
python setup.py sdist
twine upload dist/*
``` 
