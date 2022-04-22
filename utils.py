###############################################################################
# PROJECT: CVC FTM Arbitrage Bot 
# AUTHOR: Matt Hartigan
# DATE: 15-April-2022
# FILENAME: utils.py
# DESCRIPTION: Utility functions for the defi bot.
###############################################################################
import requests
import base64
import websocket
import json
from web3 import Web3
from config import config_params


# PROVIDER CONNECTIONS
def get_http_provider_connection(http, username, password):
    """ Establishes a http connection with the blockchain node defined in
    the config.py file using the python web3.py package. """
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
    """ Establishes a wss connection with the blockchain node defined in
    the config.py file using the python web3.py package. """
    w3 = Web3(Web3.WebsocketProvider(wss))
    return w3


# SETUP SMART CONTRACTS
def get_factory_contract(web3_connection, name):
    """" Returns a web3.py contract for the dex specified by the input name. """
    try:
        factory_contract_string = name + '_factory_contract'
        factory_abi_string = name + '_factory_abi'
        factory = web3_connection.eth.contract(address=config_params[factory_contract_string], abi=json.loads(config_params[factory_abi_string]))
        return factory
    except Exception as e:
        print('Error connecting ' + name + ' factory!')
        print(e)


def get_router_contract(web3_connection, name):
    try:
        router_contract_string = name + '_router_contract'
        router_abi_string = name + '_router_abi'
        router = web3_connection.eth.contract(address=config_params[router_contract_string], abi=json.loads(config_params[router_abi_string]))
        return router
    except Exception as e:
        print('Error connecting ' + name + ' router!')
        print(e)


def get_pair_contract(web3_connection, address):
    try:
        pair = web3_connection.eth.contract(address=address, abi=json.loads(config_params['standard_pair_abi']))
        return pair
    except Exception as e:
        print('Error connecting pair!')
        print(e)


def get_token_contract(web3_connection, address):
    try:
        token = web3_connection.eth.contract(address=address, abi=json.loads(config_params['standard_token_abi']))
        return token
    except Exception as e:
        print('Error connecting token!')
        print(e)
