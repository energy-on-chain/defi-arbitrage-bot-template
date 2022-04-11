###############################################################################
# PROJECT: EOC Defi Arbitrage Bot Template
# AUTHOR: Matt Hartigan
# DATE: 11-April-2022
# FILENAME: config.py
# DESCRIPTION: Defines the key parameters for a given trading bot.
###############################################################################

config_params = {
    'name': 'EOC Defi Arbitrage Bot Template',
    'version': 'v0.1.0',    # maintain versioning based on https://semver.org/
    'in_production': False,
    'frequency': 30,    # seconds
    'cloud_bucket_name': '',    # FIXME
    'cloud_bucket_path': '',    # FIXME
    'output_filename': '',    # FIXME
    'contract1': '',    # FIXME
    'contract2': '',    # FIXME
    'bet': 1000,    # size of each bet in USD
    'threshold': 0.5,
    # TODO: additional config parameters go here
}
