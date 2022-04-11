###############################################################################
# PROJECT: EOC Defi Arbitrage Bot Template
# AUTHOR: Matt Hartigan
# DATE: 11-April-2022
# FILENAME: run.py
# DESCRIPTION: Runfile that coordinates the execution of all other files for
# the EOC defi arbitrage bot. 
###############################################################################
import datetime


# AUTHENTICATE 
if config_params['in_production']:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"


# FUNCTIONS
def run():
    print(config_params['name'] + ' ' + config_params['version'] + ' is busy printing money... [' + str(datetime.datetime.utcnow()) + ']')
    print('Beginning execution... [' + str(datetime.datetime.utcnow()) + ']')
    print('Get DEX #1 quote... [' + str(datetime.datetime.utcnow()) + ']')
    print('Get DEX #2 quote... [' + str(datetime.datetime.utcnow()) + ']')
    print('Make comparison... [' + str(datetime.datetime.utcnow()) + ']')
    print('Execute trade... [' + str(datetime.datetime.utcnow()) + ']')
    print('Output results... [' + str(datetime.datetime.utcnow()) + ']')


# ENTRY POINT
if config_params['in_production']:
    schedule.every(config_params['frequency']).seconds.do(run)   
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    run()


# TODO:
# Implement spooky.py (test txn)
# Implement spirit.py (test txn)
# Implement arbitrage
# Decide whether to persist exchange connections or redo each tim
# Email notifications
# Emergency shutdown swtich
