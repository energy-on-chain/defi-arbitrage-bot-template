# Welcome to Energy On Chain's "defi-arbitrage-bot-template"!

## [ DESCRIPTION ]
This repo contains the boiler plate code for an automated trading bot that monitors defi exchanges and executes arbitrage opportunities. The user can define which exchanges to monitor (the base implementation uses Spookyswap and Spiritswap on Fantom blockchain), how frequently they would like to check, and set their own profit margin thresholds for when to take action. As long as the defi exchange you are interested in is built on the Uniswap V2 Router code (which many DEXES on EVM compatible blockchains are), you'll be able to easily add it to this project. 

## [ STACK ]
- Python (key packages include pandas, numpy, schedule)
- Google Cloud Services (for pulling and storing real-time data)

## [ BACKGROUND ]
This project was done to improve EOC's understanding of how Defi Exchange smart contracts work. In addition to implemnting a DEX arbitrage trading strategy, the lessons learned here (how to connect to a Uniswap-based DEX, query prices, execute transactions, etc.) can be extended to implement any other DEFI-based trading strategy you can think of. Feel free to take the basic ideas and run with them yourself, or get in touch to work on building your idea for a DEFI trading strategy together! 
