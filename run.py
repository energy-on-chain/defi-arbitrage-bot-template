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
def run():
    """ FIXME: function description goes here """

    # HTTP Connect to Node
    print(config_params['name'] + ' ' + config_params['version'] + ' is busy printing money... [' + str(datetime.datetime.utcnow()) + ']')
    print()
    print('Connecting to blockchain... [' + str(datetime.datetime.utcnow()) + ']')    
    web3_connection = utils.get_http_provider_connection(config_params['ftm_http'], config_params['ankr_username'], config_params['ankr_password'])    
    print()

    # Connect to DEX Routers
    print('Connecting to exchanges... [' + str(datetime.datetime.utcnow()) + ']')    # create contract objects
    exchange_name_list = [
        'spookyswap',
        'spiritswap',
    ]
    factory_contract_dict = {}
    router_contract_dict = {}
    for name in exchange_name_list:
        try:
            factory_contract_string = name + '_factory_contract'
            factory_abi_string = name + '_factory_abi'
            router_contract_string = name + '_router_contract'
            router_abi_string = name + '_router_abi'
            factory = web3_connection.eth.contract(address=config_params[factory_contract_string], abi=json.loads(config_params[factory_abi_string]))
            factory_contract_dict[name] = factory
            router = web3_connection.eth.contract(address=config_params[router_contract_string], abi=json.loads(config_params[router_abi_string]))
            router_contract_dict[name] = router
            print('Successfully connected ' + name + '!')
        except Exception as e:
            print('Error connecting ' + name + '!')
            print(e)
    print()

    # Connect to Targeted DEX Pair Contracts
    print('Connecting to pair contracts... [' + str(datetime.datetime.utcnow()) + ']')
    pair_name_list = [
        'wftm_usdc_spookyswap',
        'wftm_usdc_spiritswap',
    ]
    pair_contract_dict = {}
    for name in pair_name_list:
        try:
            contract_string = name + '_pair_contract'
            abi_string = name + '_pair_abi'
            pair_contract = web3_connection.eth.contract(address=config_params[contract_string], abi=json.loads(config_params[abi_string]))
            pair_contract_dict[name] = pair_contract
            print('Successfully connected ' + name + '!')
        except Exception as e:
            print('Error connecting ' + name + ' pair!')
            print(e)
    print()

    # Collect Prices
    print('FIXME: Checking prices... [' + str(datetime.datetime.utcnow()) + ']')
    pair0 = web3_connection.eth.contract(address=config_params['wftm_usdc_spookyswap_pair_contract'], abi=json.loads(config_params['wftm_usdc_spookyswap_pair_abi']))
    factory0 = web3_connection.eth.contract(address=config_params['spookyswap_factory_contract'], abi=json.loads(config_params['spookyswap_factory_abi']))
    router0 = web3_connection.eth.contract(address=config_params['spookyswap_router_contract'], abi=json.loads(config_params['spookyswap_router_abi']))
    pair1 = web3_connection.eth.contract(address=config_params['wftm_usdc_spiritswap_pair_contract'], abi=json.loads(config_params['wftm_usdc_spiritswap_pair_abi']))
    factory1 = web3_connection.eth.contract(address=config_params['spiritswap_factory_contract'], abi=json.loads(config_params['spiritswap_factory_abi']))
    router1 = web3_connection.eth.contract(address=config_params['spiritswap_router_contract'], abi=json.loads(config_params['spiritswap_router_abi']))
    # print(pair0.all_functions())
    reserves0 = pair0.functions.getReserves().call()
    token00 = pair0.functions.token0().call()
    token01 = pair0.functions.token1().call()
    reserves1 = pair1.functions.getReserves().call()
    token10 = pair1.functions.token0().call()
    token11 = pair1.functions.token1().call()
    # print(router.functions.getAmountIn(1, reserves[1], reserves[0]).call())
    print('Current Spooky USDC (' + token00 + ') reserves = ' + str(reserves0[0] / 10**6) + ' coins total') 
    print('Current Spooky FTM (' + token01 + ') reserves = ' + str(reserves0[1] / 10**18) + ' coins total') 
    print('Price w/o fees: 1 USDC = ' + str(round((reserves0[1] / 10**18) / (reserves0[0] / 10**6), 5)) + ' FTM on spooky currently')
    print('Price w/o fees: 1 FTM = ' + str(round((reserves0[0] / 10**6) / (reserves0[1] / 10**18), 5)) + ' USDC on spooky currently')
    amount_out0 = router0.functions.getAmountOut(1, reserves0[0], reserves0[1]).call()
    amount_in0 = router0.functions.getAmountIn(1, reserves0[1], reserves0[0]).call()
    ftm_per_usdc_spooky = amount_out0 / 10**12
    usdc_per_ftm_spooky = 1 / (amount_in0 / 10**12)
    print('Price with fees: 1 USDC returns ' + str(round(ftm_per_usdc_spooky, 5)) + ' FTM coins')
    print('Price with fees: 1 FTM returns ' + str(round(usdc_per_ftm_spooky, 5)) + ' USDC coins')
    print()
    print('Current Spirit USDC (' + token10 + ') reserves = ' + str(reserves1[0] / 10**6) + ' coins total') 
    print('Current Spirit FTM (' + token11 + ') reserves = ' + str(reserves1[1] / 10**18) + ' coins total') 
    print('Price w/o fees: 1 USDC = ' + str(round((reserves1[1] / 10**18) / (reserves1[0] / 10**6), 5)) + ' FTM on spirit currently')
    print('Price w/o fees: 1 FTM =  ' + str(round((reserves1[0] / 10**6) / (reserves1[1] / 10**18), 5)) + ' USDC on spirit currently')
    amount_out1 = router1.functions.getAmountOut(1, reserves1[0], reserves1[1]).call()
    amount_in1 = router1.functions.getAmountIn(1, reserves1[1], reserves1[0]).call()
    ftm_per_usdc_spirit = amount_out1 / 10**12
    usdc_per_ftm_spirit = 1 / (amount_in1 / 10**12)
    print('Price with fees: 1 USDC returns ' + str(round(ftm_per_usdc_spirit, 5)) + ' FTM coins')
    print('Price with fees: 1 FTM returns ' + str(round(usdc_per_ftm_spirit, 5)) + ' USDC coins')
    print()

    # Check Arbitrage Opportunities
    print('FIXME: Checking arbitrage... [' + str(datetime.datetime.utcnow()) + ']')    # look for arbitrage
    ftm_spread = ftm_per_usdc_spooky - ftm_per_usdc_spirit
    usdc_spread = usdc_per_ftm_spooky - usdc_per_ftm_spirit
    cheapest_ftm_exchange = ''
    if ftm_spread > 0:
        cheapest_ftm_exchange = 'spooky'
    else:
        cheapest_ftm_exchange = 'spirit'
    cheapest_usdc_exchange = ''
    if usdc_spread > 0:
        cheapest_usdc_exchange = 'spooky'
    else:
        cheapest_usdc_exchange = 'spirit'
    print('FTM spread = ' + str(abs(ftm_spread)) + ' and it is cheapest on ' + cheapest_ftm_exchange)
    print('USDC spread = ' + str(abs(usdc_spread)) + ' and it is cheapest on ' + cheapest_usdc_exchange)
    ftm_profitability = abs(ftm_spread) * config_params['bet']
    usdc_profitability = abs(usdc_spread) * config_params['bet']
    print('We can gain ' + str(ftm_profitability) + ' FTM by moving ' + str(config_params['bet']) + ' USDC coins')
    print('We can gain ' + str(usdc_profitability) + ' USDC by moving ' + str(config_params['bet']) + ' FTM coins')
    print()

    # Execute Trades
    print('FIXME: Executing trades... [' + str(datetime.datetime.utcnow()) + ']')
    print()
    # Output Results
    print('FIXME: Outputting results... [' + str(datetime.datetime.utcnow()) + ']')
    print()
    # Finish
    print('Run complete! [' + str(datetime.datetime.utcnow()) + ']')
    print()

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
# Query raw spooky price (DONE)
# Query raw spirit price (DONE)
# Calc exchange fees, add slippage, add blockchain transaction fees (DONE)
# Rough in the arbitrage logic (DONE)


# TODO:
# Convert from http to wss feed(?)... need to talk to ankr.com
# Make single transaction on spooky
# Make single transaction on spirit
# Make single arbitrage transaction, verify the result matches the estimated output
# Move from single transaction to a loop
# Write tility func for calculating equivalent usd and comparing to min profitability threshold
# Convert price checks to dynamic logic
# Convert arbitrage checks to dynamic logic
# Setup results output (gcfs csv, dash)
# Deploy to mini vm
# FUTURE: Consider putting coins in farm in the intermediate time between swaps
# FUTURE: COB to AMM mixed arb
