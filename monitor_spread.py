###############################################################################
# PROJECT: CVC FTM Arbitrage Bot 
# AUTHOR: Matt Hartigan
# DATE: 22-April-2022
# FILENAME: monitor_spread.py
# DESCRIPTION: Reads in the final list of pairs that will be potentially 
# arbitraged between the two exchanges. Every X seconds, queries what the
# spread is and stores that data over time so we can evaluate which are the 
# most profitable later on.
###############################################################################
import os
import datetime
import utils
import json
import time
import schedule
import pandas as pd
from config import config_params


# AUTHENTICATE 
# if config_params['in_production']:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"


# FUNCTIONS
def get_all_spreads():
    web3_connection = utils.get_http_provider_connection(config_params['ftm_http'], config_params['ankr_username'], config_params['ankr_password'])    # connect to FTM node
    router0 = web3_connection.eth.contract(address=config_params['spiritswap_router_contract'], abi=json.loads(config_params['spiritswap_router_abi']))
    router1 = web3_connection.eth.contract(address=config_params['spookyswap_router_contract'], abi=json.loads(config_params['spookyswap_router_abi']))
    
    # Load all pairs being monitored
    pair_df = pd.read_csv('output/all_overlapping_pairs_test.csv')   
    spread_df = pair_df.copy()

    # Update reserves
    spread_df['spiritswap_token0_reserves'] = spread_df['spiritswap_pair_contract'].apply(lambda x: web3_connection.eth.contract(address=x, abi=json.loads(config_params['standard_pair_abi'])).functions.getReserves().call()[0])
    spread_df['spiritswap_token1_reserves'] = spread_df['spiritswap_pair_contract'].apply(lambda x: web3_connection.eth.contract(address=x, abi=json.loads(config_params['standard_pair_abi'])).functions.getReserves().call()[1])
    spread_df['spiritswap_reserves_timestamp'] = spread_df['spiritswap_pair_contract'].apply(lambda x: web3_connection.eth.contract(address=x, abi=json.loads(config_params['standard_pair_abi'])).functions.getReserves().call()[2])
    spread_df['spookyswap_token0_reserves'] = spread_df['spookyswap_pair_contract'].apply(lambda x: web3_connection.eth.contract(address=x, abi=json.loads(config_params['standard_pair_abi'])).functions.getReserves().call()[0])
    spread_df['spookyswap_token1_reserves'] = spread_df['spookyswap_pair_contract'].apply(lambda x: web3_connection.eth.contract(address=x, abi=json.loads(config_params['standard_pair_abi'])).functions.getReserves().call()[1])
    spread_df['spookyswap_reserves_timestamp'] = spread_df['spookyswap_pair_contract'].apply(lambda x: web3_connection.eth.contract(address=x, abi=json.loads(config_params['standard_pair_abi'])).functions.getReserves().call()[2])

    # Calculate amounts in and out
    spread_df['spiritswap_amountin'] = spread_df.apply(lambda x: router0.functions.getAmountIn(1, x['spiritswap_token1_reserves'], x['spiritswap_token0_reserves']).call(), axis=1)
    spread_df['spiritswap_amountout'] = spread_df.apply(lambda x: router0.functions.getAmountOut(1, x['spiritswap_token0_reserves'], x['spiritswap_token1_reserves']).call(), axis=1)
    spread_df['spookyswap_amountin'] = spread_df.apply(lambda x: router1.functions.getAmountIn(1, x['spookyswap_token1_reserves'], x['spookyswap_token0_reserves']).call(), axis=1)
    spread_df['spookyswap_amountout'] = spread_df.apply(lambda x: router1.functions.getAmountOut(1, x['spookyswap_token0_reserves'], x['spookyswap_token1_reserves']).call(), axis=1)

    # Calculate rates
    spread_df['spiritswap_token0_per_token1'] = spread_df.apply(lambda x: (x['spiritswap_amountout'] * (10**x['spiritswap_token0_decimals'])) / (10**x['spiritswap_token1_decimals']), axis=1)
    spread_df['spiritswap_token1_per_token0'] = spread_df.apply(lambda x: (10**x['spiritswap_token1_decimals']) / (x['spiritswap_amountin'] * (10**x['spiritswap_token0_decimals'])), axis=1)
    spread_df['spookyswap_token0_per_token1'] = spread_df.apply(lambda x: (x['spookyswap_amountout'] * (10**x['spookyswap_token0_decimals'])) / (10**x['spookyswap_token1_decimals']), axis=1)
    spread_df['spookyswap_token1_per_token0'] = spread_df.apply(lambda x: (10**x['spookyswap_token1_decimals']) / (x['spookyswap_amountin'] * (10**x['spookyswap_token0_decimals'])), axis=1)

    # Correct reserves with token count
    spread_df['spiritswap_token0_reserves'] = spread_df['spiritswap_token0_reserves'] / spread_df['spiritswap_token0_decimals']
    spread_df['spiritswap_token1_reserves'] = spread_df['spiritswap_token1_reserves'] / spread_df['spiritswap_token1_decimals']
    spread_df['spookyswap_token0_reserves'] = spread_df['spookyswap_token0_reserves'] / spread_df['spookyswap_token0_decimals']
    spread_df['spookyswap_token1_reserves'] = spread_df['spookyswap_token1_reserves'] / spread_df['spookyswap_token1_decimals']

    # Calculate spreads
    spread_df['token0_spread'] = spread_df.apply(lambda x: x['spiritswap_token0_per_token1'] - x['spookyswap_token0_per_token1'], axis=1)
    spread_df['token1_spread'] = spread_df.apply(lambda x: x['spiritswap_token1_per_token0'] - x['spookyswap_token1_per_token0'], axis=1)
    spread_df['pair_name'] = spread_df['spiritswap_token0_symbol'] + spread_df['spiritswap_token1_symbol']

    # Drop unneeded columns
    # FIXME: n/a for now

    # Output individual spread histories
    new_history_df = spread_df[['pair_name', 'token0_spread', 'token1_spread', 'spiritswap_token0_per_token1', 'spiritswap_token1_per_token0', 'spookyswap_token0_per_token1', 'spookyswap_token1_per_token0', 'spiritswap_reserves_timestamp']]
    new_history_df['utc'] = new_history_df['spiritswap_reserves_timestamp'].apply(lambda x: datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    new_history_df_list = new_history_df.values.tolist()
    for pair_list in new_history_df_list:
        filename = 'output/' + pair_list[0] + '_spread_history.csv'
        old_history_df = pd.read_csv(filename)    # load old data
        old_history_df.loc[len(old_history_df)] = pair_list 
        old_history_df.to_csv(filename, index=False)

    # Output summary of average spreads for each pair being watched
    summary_cols = ['pair_name', 'token0_spread', 'token1_spread', 'spiritswap_token0_per_token1', 'spiritswap_token1_per_token0', 'spookyswap_token0_per_token1', 'spookyswap_token1_per_token0']
    full_summary_df = pd.DataFrame(columns=summary_cols)
    
    file_list = os.listdir('output/')
    for filename in file_list:
        if '_spread_history.csv' in filename:
            summary_list = []
            df = pd.read_csv('output/' + filename)
            df[['token0_spread', 'token1_spread']] = df[['token0_spread', 'token1_spread']].abs()
            summary_list = df[['token0_spread', 'token1_spread', 'spiritswap_token0_per_token1', 'spiritswap_token1_per_token0', 'spookyswap_token0_per_token1', 'spookyswap_token1_per_token0']].mean().tolist()    # get mean values
            summary_list = [df['pair_name'].iloc[0]] + summary_list    # add pair name
            print(summary_list)
            full_summary_df.loc[len(full_summary_df)] = summary_list
            print(full_summary_df)
    
    full_summary_df.to_csv('output/spread_history_summary.csv', index=False)


# ENTRY POINT
if config_params['in_production']:
    schedule.every(config_params['monitor_frequency']).seconds.do(get_all_spreads)   
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    get_all_spreads()
    

# TODO:
# Track spreads over time for the desired coins (need a new output file and/or format)
#
