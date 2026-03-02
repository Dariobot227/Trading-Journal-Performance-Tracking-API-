# Trading Journal & Performance Tracking API

A Django REST API serving as a digital trading journal where traders can log, manage, and analyze their activity in an isolated environment. It enables users to track strategies and emotions while generating automated performance metrics like net profit and win/loss ratios.

## Features

- Create, update, and delete trades
- Log trading strategies for each trade
- Track emotions and performance metrics
- User authentication (token-based)
- Filtering and querying trades by date, strategy, or outcome
- overall trade summaries showing total number of trades taken and netprofit or net-loss made for that particular account

## API DOCUMENTATION
HERE are the endpoints to use
User authentication
|Method  |         |     Endpoint  |                   |   Description                |        Auth Required|

|POST              | /api/auth/register/ |             | Register a new user            |     No |
|POST              |/api/login/         |               |exiting user login              |    Yes|


Strategy Endpoints
POST           /api/strategies/                    Create a strategy                     Yes
GET           /api/strategies/                     List strategies                       Yes
PUT          /api/strategies/{id}/                 Update a strategy                     Yes
DELETE       /api/strategies/{id}/                 Delete a strategy                     Yes

Trade Endpoints
POST            /api/trades/                       Create a trade                        Yes
GET           /api/trades/ –                       List user trades                      Yes
GET           /api/trades/{id}/ –                  Retrieve a single trade               Yes
PUT           /api/trades/{id}/ –                  Update a trade                        Yes
DELETE        /api/trades/{id}/ –                  Delete a trade                        Yes

Analytics Endpoint
GET /api/trades/summary/ – View performance summary (total trades, net profit)


## Tech Stack

- **Backend:** Django 6.x, Django REST Framework  
- **Database:** PostgreSQL (default: SQLite for development)  
- **Environment Management:** `python-dotenv`, `.env`  
- **Version Control:** Git + GitHub  


# profit or loss formulae

For BUYS doesnt matter the pair
Profit = (Exit Price - Entry Price) × Lot Size × Contract Size

For SELLS:
Profit = (Entry Price - Exit Price)× Lot Size × Contract Size

# Contract Size Formula:
WHAT IS CONTRACT_SIZE
Contract Size = Market Defined Asset Unit Value

Examples:
XAUUSD = 100 ounces
EURUSD = 100000 units
BTCUSD = 1 contract

