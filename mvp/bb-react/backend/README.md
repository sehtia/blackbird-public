# Blackbird Backend

## Setup

Install all the relevant python dependencies using the following command:
`python3 -m pip install -r requirements.txt `

## Local Testing

1. Send request to backend server
`curl "localhost:5000/walletData?walletAddress={addy here}"`

1. How to get the price of crypto in differenct currencies
`curl "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR"`

## Server Setup

To send requests to server use the following command:

`curl https://gradient.pythonanywhere.com/prubby`

To push updates to the server, follow instructions below:

1. Ensure wsgi file is pointing to correct directory (where the main.py file lives)
1. Ensure working directory and code directory are correct
1. Either nuke all files and clone from github or pull from head. Who gaf
1. Smash that mf reload button


## Scraping Wallet Addresses

```
>>> import requests
>>> import pandas
>>> r = requests.get("https://www.coincarp.com/currencies/ethereum/richlist/")
>>> x = pandas.read_html(r.text)
>>> x = x[0]
>>> x["prub"] = x["Address.1"].apply(lambda a: a[:a.find(" ")] if " " in a else a)
>>> x.to_csv("boobs.csv")
```
