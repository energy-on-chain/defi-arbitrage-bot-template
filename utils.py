###############################################################################
# PROJECT: EOC Defi Arbitrage Bot Template
# AUTHOR: Matt Hartigan
# DATE: 15-April-2022
# FILENAME: utils.py
# DESCRIPTION: Utility functions for the defi bot.
###############################################################################
import requests
import base64
import websocket
from web3 import Web3


# PROVIDER CONNECTIONS
def get_http_provider_connection(http, username, password):
    session = requests.Session()
    encoded_login = username + ':' + password
    encoded_login = encoded_login.encode('ascii')
    b64 = base64.b64encode(encoded_login).decode('ascii')
    session.headers.update({'Authorization': 'Basic ' + b64})
    w3 = Web3(Web3.HTTPProvider(http, session=session))
    if w3.isConnected():
        print('Successfully established FTM web3 http connection!')
    else:
        print('Error establishing Web3 Connection!')
    return w3


def get_wss_provider_connection(wss):
    w3 = Web3(Web3.WebsocketProvider(wss))
    return w3


def get_account_balance(web3_connection, address):
    balance = web3_connection.eth.get_balance(address)
    print(balance)
    return(balance)
