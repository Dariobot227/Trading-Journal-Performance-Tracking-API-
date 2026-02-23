# Trading Journal & Performance Tracking API

A backend-only Django REST API that allows traders to log, manage, and analyze their trading activity.  
This API acts as a **digital trading journal**, helping users record trades, associate them with strategies, track emotions, and view performance summaries such as total trades, net profit, and win/loss ratio.

---

## Table of Contents

- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Project Structure](#project-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Environment Variables](#environment-variables)  
- [Usage](#usage)  
- [API Endpoints](#api-endpoints)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Create, update, and delete trades
- Log trading strategies for each trade
- Track emotions and performance metrics
- User authentication (token-based)
- Filtering and querying trades by date, strategy, or outcome
- Secure configuration using `.env` and `security.py`
- Ready for development, testing, and production environments

---

## Tech Stack

- **Backend:** Django 6.x, Django REST Framework  
- **Database:** PostgreSQL (default: SQLite for development)  
- **Environment Management:** `python-dotenv`, `.env`  
- **Version Control:** Git + GitHub  
- **Optional:** Docker for containerized deployments

---

## Project Structure

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

