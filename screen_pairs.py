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
    print("Getting list of all available pair contracts from " + str(exchange) + '...')
    factory = utils.get_factory_contract(web3_connection, exchange)    # create dex factory smart contract instance
    pairs_length_dict = {}  
    pairs_list = []
    counter = 0
    print(factory.functions.allPairsLength().call())
    print()
    while counter < factory.functions.allPairsLength().call():    
        pairs_list.append(factory.functions.allPairs(counter).call())
        print('Pair at index' + str(counter) + ' collected')
        counter = counter + 1
    return pairs_list


def get_initial_pair_data(web3_connection, pair_contract, prefix):
    """ Returns a bare bones list of information corresponding to the pair contract at the input address. """
    pair_data_dict = {}
    
    pair = utils.get_pair_contract(web3_connection, pair_contract)
    try:
        pair_data_dict[prefix + 'pair_type'] = pair.functions.name().call()
        pair_data_dict[prefix + 'pair_contract'] = pair_contract
        pair_data_dict[prefix + 'pair_total_supply'] = pair.functions.totalSupply().call()
    except Exception as e:
        print('There was an error in get_initial_pair_data collecting pair info.')
        print(e)
        pair_data_dict[prefix + 'pair_type'] = 'Error'
        pair_data_dict[prefix + 'pair_contract'] = 'Error'
        pair_data_dict[prefix + 'pair_total_supply'] = 'Error'

    token0 = utils.get_token_contract(web3_connection, pair.functions.token0().call())
    try:
        pair_data_dict[prefix + 'token0_name'] = token0.functions.name().call()
        pair_data_dict[prefix + 'token0_symbol'] = token0.functions.symbol().call()
        pair_data_dict[prefix + 'token0_contract'] = pair.functions.token0().call()
        pair_data_dict[prefix + 'token0_reserves'] = pair.functions.getReserves().call()[0]
        pair_data_dict[prefix + 'token0_total_supply'] = token0.functions.totalSupply().call()
        pair_data_dict[prefix + 'token0_decimals'] = token0.functions.decimals().call()
    except Exception as e:
        print('There was an error in get_initial_pair_data collecting token0 info.')
        print(e)
        pair_data_dict[prefix + 'token0_name'] = 'Error'
        pair_data_dict[prefix + 'token0_symbol'] = 'Error'
        pair_data_dict[prefix + 'token0_contract'] = 'Error'
        pair_data_dict[prefix + 'token0_reserves'] = 'Error'
        pair_data_dict[prefix + 'token0_total_supply'] = 'Error'
        pair_data_dict[prefix + 'token0_decimals'] = 'Error'

    token1 = utils.get_token_contract(web3_connection, pair.functions.token1().call())
    try:
        pair_data_dict[prefix + 'token1_name'] = token1.functions.name().call()
        pair_data_dict[prefix + 'token1_symbol'] = token1.functions.symbol().call()
        pair_data_dict[prefix + 'token1_contract'] = pair.functions.token1().call()
        pair_data_dict[prefix + 'token1_reserves'] = pair.functions.getReserves().call()[1]
        pair_data_dict[prefix + 'token1_total_supply'] = token1.functions.totalSupply().call()
        pair_data_dict[prefix + 'token1_decimals'] = token1.functions.decimals().call()

    except Exception as e:
        print('There was an error in get_initial_pair_data collecting token1 info.')
        print(e)
        pair_data_dict[prefix + 'token1_name'] = 'Error'
        pair_data_dict[prefix + 'token1_symbol'] = 'Error'
        pair_data_dict[prefix + 'token1_contract'] = 'Error'
        pair_data_dict[prefix + 'token1_reserves'] = 'Error'
        pair_data_dict[prefix + 'token1_decimals'] = 'Error'
        pair_data_dict[prefix + 'token1_total_supply'] = 'Error'

    return pair_data_dict


def get_overlapping_pairs(filename0, filename1, prefix0, prefix1):
    """ Reads in the list of coin pairs from the two input exchange csv's and outputs a new csv of all the matches. """
    df0 = pd.read_csv(filename0)
    df1 = pd.read_csv(filename1)
    df0['combo01'] = df0[prefix0 + 'token0_contract'] + df0[prefix0 + 'token1_contract']
    df1['combo01'] = df1[prefix1 + 'token0_contract'] + df1[prefix1 + 'token1_contract']
    merged_df01 = pd.merge(df0, df1, on='combo01')
    merged_df01.drop(['combo01'], axis=1, inplace=True)
    print(merged_df01)

    df0 = pd.read_csv(filename0)
    df1 = pd.read_csv(filename1)
    df0['combo10'] = df0[prefix0 + 'token1_contract'] + df0[prefix0 + 'token0_contract']
    df1['combo10'] = df1[prefix1 + 'token1_contract'] + df1[prefix1 + 'token0_contract']
    merged_df10 = pd.merge(df0, df1, on='combo10')
    merged_df10.drop(['combo10'], axis=1, inplace=True)
    print(merged_df10)

    combo_df = pd.concat([merged_df01, merged_df10], axis=0)
    print(combo_df)
    combo_df.drop_duplicates(keep='first', inplace=True)
    print(combo_df)
    combo_df.to_csv('output/all_overlapping_pairs.csv', index=False)


# ENTRY POINT
# Connect web3
web3_connection = utils.get_http_provider_connection(config_params['ftm_http'], config_params['ankr_username'], config_params['ankr_password'])    # connect to FTM node

# Get exchange 1 pairs
# spiritswap_pair_list = get_all_pairs(web3_connection, "spiritswap")    # get available pair data on spirit
# spiritswap_pair_data_list = []
# spiritswap_counter = 0
# for pair in spiritswap_pair_list:
#     print('Collecting data for pair: ' + str(pair) + ' at index ' + str(spiritswap_counter) + ' on spiritswap.')
#     spiritswap_pair_data_list.append(get_initial_pair_data(web3_connection, pair, 'spiritswap_'))
#     spiritswap_counter = spiritswap_counter + 1
# spiritswap_pair_df = pd.DataFrame(spiritswap_pair_data_list)
# spiritswap_pair_df.to_csv('output/spiritswap_all_pairs.csv', index=False)

# Get exchange 2 pairs
# spookyswap_pair_list = get_all_pairs(web3_connection, "spookyswap")    # get available pair data on spooky
# spookyswap_pair_data_list = []
# spookyswap_counter = 7000
# for pair in spookyswap_pair_list[7000:14000]:
#     print('Collecting data for pair: ' + str(pair) + ' at index ' + str(spookyswap_counter) + ' on spookyswap.')
#     spookyswap_pair_data_list.append(get_initial_pair_data(web3_connection, pair, 'spookyswap_'))
#     spookyswap_counter = spookyswap_counter + 1
# spookyswap_pair_df = pd.DataFrame(spookyswap_pair_data_list)
# spookyswap_pair_df.to_csv('output/spookywap_all_pairs2.csv', index=False)

# Find overlapping pairs
get_overlapping_pairs('output/spiritswap_all_pairs.csv', 'output/spookywap_all_pairs.csv', 'spiritswap_', 'spookyswap_')


# TODO:
# Add filters
