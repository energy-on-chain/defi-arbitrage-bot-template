###############################################################################
# PROJECT: CVC FTM Arbitrage Bot 
# AUTHOR: Matt Hartigan
# DATE: 20-April-2022
# FILENAME: screen_pairs.py
# DESCRIPTION: Identifies all available overlapping pairs on the specified 
# exchanges and uses a series of screening functions to shorten the list to 
# a manageable, most profitable size that can be used for monitoring the 
# average spread, executing arbitrage, etc.
###############################################################################
import datetime
import utils
import json
import pandas as pd
from config import config_params


# AUTHENTICATE 
# if config_params['in_production']:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"


# FUNCTIONS
def get_all_pairs(web3_connection, exchange):
    """ Returns a list of the pair contracts for all the available pairs on the input exchange. """
    factory = utils.get_factory_contract(web3_connection, exchange)    # create dex factory smart contract instance
    pairs_length_dict = {}  
    pairs_list = []
    counter = 0
    while counter < factory.functions.allPairsLength().call():    
    # while counter < 5:    # FIXME: for dev only
        print(counter)
        pairs_list.append(factory.functions.allPairs(counter).call())
        counter = counter + 1
    return pairs_list


def get_initial_pair_data(web3_connection, pair_contract):
    """ Returns a bare bones list of information corresponding to the pair contract at the input address. """
    pair = utils.get_pair_contract(web3_connection, pair_contract)

    pair_data_dict = {}
    pair_data_dict['pair_type'] = pair.functions.name().call()
    pair_data_dict['pair_contract'] = pair_contract
    pair_data_dict['pair_total_supply'] = pair.functions.totalSupply().call()

    token0 = utils.get_token_contract(web3_connection, pair.functions.token0().call())
    pair_data_dict['token0_name'] = token0.functions.name().call()
    pair_data_dict['token0_symbol'] = token0.functions.symbol().call()
    pair_data_dict['token0_contract'] = pair.functions.token0().call()
    pair_data_dict['token0_reserves'] = pair.functions.getReserves().call()[0]
    pair_data_dict['token0_total_supply'] = token0.functions.totalSupply().call()
    pair_data_dict['token0_decimals'] = token0.functions.decimals().call()

    token1 = utils.get_token_contract(web3_connection, pair.functions.token1().call())
    pair_data_dict['token1_name'] = token1.functions.name().call()
    pair_data_dict['token1_symbol'] = token1.functions.symbol().call()
    pair_data_dict['token1_contract'] = pair.functions.token1().call()
    pair_data_dict['token1_reserves'] = pair.functions.getReserves().call()[1]
    pair_data_dict['token1_decimals'] = token1.functions.decimals().call()
    pair_data_dict['token1_total_supply'] = token1.functions.totalSupply().call()

    return pair_data_dict


def get_overlapping_pairs(filename0, filename1):
    """ Reads in the list of coin pairs from the two input exchange csv's and outputs a new csv of all the matches. """
    df0 = pd.read_csv(filename0)
    df1 = pd.read_csv(filename1)

    df0['combo01'] = df0['token0_contract'] + df0['token1_contract']
    df1['combo01'] = df1['token0_contract'] + df1['token1_contract']
    df0['combo10'] = df0['token1_contract'] + df0['token0_contract']
    df1['combo10'] = df1['token1_contract'] + df1['token0_contract']
    
    merged_df01 = df0[df0.combo01.isin(df1['combo01'].tolist())]    # find token0+token1 type matches
    merged_df10 = df0[df0.combo10.isin(df1['combo10'].tolist())]    # find token1+token0 type matches

    combo_df = pd.concat([merged_df01, merged_df10], axis=0)
    print(combo_df)
    combo_df.drop_duplicates(keep='first', inplace=True)
    combo_df.drop(['combo01', 'combo10'], axis=1, inplace=True)
    print(combo_df)
    combo_df.to_csv('output/all_overlapping_pairs.csv', index=False)


# ENTRY POINT
# Connect web3
web3_connection = utils.get_http_provider_connection(config_params['ftm_http'], config_params['ankr_username'], config_params['ankr_password'])    # connect to FTM node

# Get exchange 1 pairs
spiritswap_pair_list = get_all_pairs(web3_connection, "spiritswap")    # get available pair data on spirit
spiritswap_pair_data_list = []
for pair in spiritswap_pair_list:
    spiritswap_pair_data_list.append(get_initial_pair_data(web3_connection, pair))
spiritswap_pair_df = pd.DataFrame(spiritswap_pair_data_list)
spiritswap_pair_df.to_csv('output/spiritswap_all_pairs.csv', index=False)

# Get exchange 2 pairs
spookyswap_pair_list = get_all_pairs(web3_connection, "spookyswap")    # get available pair data on spooky
spookyswap_pair_data_list = []
for pair in spookyswap_pair_list:
    spookyswap_pair_data_list.append(get_initial_pair_data(web3_connection, pair))
spookyswap_pair_df = pd.DataFrame(spookyswap_pair_data_list)
spookyswap_pair_df.to_csv('output/spookywap_all_pairs.csv', index=False)

# Find overlapping pairs
get_overlapping_pairs('output/spiritswap_all_pairs.csv', 'output/spookywap_all_pairs.csv')

# Filter pairs by...
# FIXME: liquidity
# FIXME: other...


# TODO:
