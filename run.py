###############################################################################
# PROJECT: EOC Defi Arbitrage Bot Template
# AUTHOR: Matt Hartigan
# DATE: 11-April-2022
# FILENAME: run.py
# DESCRIPTION: Runfile that coordinates the execution of all other files for
# the EOC defi arbitrage bot. 
###############################################################################
import datetime
import utils
import json
from config import config_params
from exchanges import spooky


# AUTHENTICATE 
# if config_params['in_production']:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"


# FUNCTIONS
def check_spookyswap_to_spiritswap(web3_connection, factory, router, token0_symbol, token0_address, token1_symbol, token1_address, pair_address, pair_abi):
    """ FIXME: function description goes here """
    queried_pair_address = factory.functions.getPair(token0_address, token1_address).call()    # get the contract address for the desired exchange pair

    if queried_pair_address == pair_address:
        print('Token pair contract addresses match!')
        pair_contract = web3_connection.eth.contract(address=pair_address, abi=pair_abi)    # instantiate the exchange pair contract
        # pair_swap_filter = pair_contract.
        max_token1_for_token0 = router.functions.getAmountOut().call()
    else:
        print('Addresses do not match!')
        exit(0)
    
    print(pair_contract.all_functions())
    print(router.all_functions())
    # print(factory.all_functions())


def run():
    """ FIXME: function description goes here """

    # HTTP Connect to Node
    print(config_params['name'] + ' ' + config_params['version'] + ' is busy printing money... [' + str(datetime.datetime.utcnow()) + ']')
    print('Connecting to blockchain... [' + str(datetime.datetime.utcnow()) + ']')    
    web3_connection = utils.get_http_provider_connection(config_params['ftm_http'], config_params['ankr_username'], config_params['ankr_password'])    
    # web3_connection = utils.get_wss_provider_connection(config_params['ftm_wss'])    # wss connect to a web3 provider

    # Connect to DEX Routers
    print('Loading contracts... [' + str(datetime.datetime.utcnow()) + ']')    # create contract objects
    spookyswap_factory_contract = web3_connection.eth.contract(address=config_params['spookyswap_factory_contract'], abi=json.loads(config_params['spookyswap_factory_abi']))    # create spookyswap exchange contract
    spookyswap_router_contract = web3_connection.eth.contract(address=config_params['spookyswap_router_contract'], abi=json.loads(config_params['spookyswap_router_abi']))    # create spookyswap exchange contract
    spiritswap_factory_contract = web3_connection.eth.contract(address=config_params['spiritswap_factory_contract'], abi=json.loads(config_params['spiritswap_factory_abi']))    # create spiritswap exchange contract
    spiritswap_router_contract = web3_connection.eth.contract(address=config_params['spiritswap_router_contract'], abi=json.loads(config_params['spiritswap_router_abi']))    # create spiritswap exchange contract
    print('Spoookyswap available functions:')
    print(spookyswap_router_contract.all_functions())
    print('Spiritswap available functions:')
    print(spiritswap_router_contract.all_functions())
    print()

    # Connect to Targeted DEX Pair Contracts
    # FIXME

    # Check for Arbitrage
    print('Checking for arbitrage... [' + str(datetime.datetime.utcnow()) + ']')    # look for arbitrage
    try:
        print('Spookyswap...')
        # check_spookyswap_to_spiritswap(web3_connection, spookyswap_factory_contract, spookyswap_router_contract, 'WFTM', config_params['wftm_contract'], 'USDC', config_params['usdc_contract'], config_params['wftm_usdc_spookyswap_pair_contract'], config_params['wftm_usdc_spookyswap_pair_abi'])
        
        print('Spiritswap...')
    except Exception as e:
        print('FIXME: There was an error during the check for arbitrage process!')
        print(e)

    print('Executing trades... [' + str(datetime.datetime.utcnow()) + ']')
    print('Outputting results... [' + str(datetime.datetime.utcnow()) + ']')


# ENTRY POINT
if config_params['in_production']:
    schedule.every(config_params['frequency']).seconds.do(run)   
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    run()


# COMPLETED:
# Setup framework for defi bot (DONE)
# Setup config file with appropriate contracts (DONE)
# Setup node connection to FTM blockchain (DONE)
# Connect to and query spookyswap factory and router (DONE)
# Connect to and query spiritswap factory and router (DONE)


# TODO:
# convert to wss feed(?)
# figure out how to calculate price on univ2
# make first auto transaction from spooky and spirit
# setup arbitrage logic
# setup results output (gcfs csv, dash)
# deploy to vm
# Consider putting it in a farm in the intermediate time between swaps
