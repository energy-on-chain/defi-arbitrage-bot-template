###############################################################################
# PROJECT: EOC Defi Arbitrage Bot Template
# AUTHOR: Matt Hartigan
# DATE: 11-April-2022
# FILENAME: config.py
# DESCRIPTION: Handles interface with spookyswap.finance
###############################################################################
import requests
import base64
import websocket
from web3 import Web3


# CONFIG
factory_contract = '0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3'
router_contract = '0xF491e7B69E4244ad4002BC14e878a34207E38c29'
boo_contract = '0x841FAD6EAe12c286d1Fd18d1d525DFfA75C7EFFE'
wftm_contract = '0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83'
ftm_boo_contract = '0xEc7178F4C41f346b2721907F5cF7628E388A7a58'


# TODO:
# track tvl
# get price quote for different assets
# track transaction volume
# listen for new pools (what other info can we get off these dexes?)
# make a trade
