## Customer CRM
I built this as part of my Python learning journey. It's a CRM system for e-commerce businesses — 
something I actually needed for my own Amazon and Shopify stores.

## What it does
- Add and manage customers
- Track products and prices
- Log orders and their status (completed, returned, cancelled, chargeback)
- Record customer complaints and communications
- Track email threads with customers
- Store product reviews and ratings
- Generate business reports like most returned products, chargebacks, top sellers

## Why I built it
I run multiple e-commerce stores and wanted a simple way to track customer issues, 
returns and communications in one place. This project also helped me practice Python, 
SQLite databases, and how to structure a real multi-file project.

## Tech used
- Python 3
- SQLite — for storing all the data
- No frameworks — just pure Python and the standard library

## Project files
db.py # sets up all 6 database tables
customer.py # customer functions
product.py # product functions
order.py # order functions
comms.py # communication functions
emails.py # email functions
reviews.py # review functions
reports.py # business reports
main.py # runs everything

## How to run it
```bash
git clone https://github.com/MAK1005/Customer-Crm.git
cd Customer-Crm
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## What I want to add next
- Connect it to Shopify API so orders sync automatically
- Add a simple web interface
- Export reports to CSV so I can open them in Excel

## About me
I built this project while learning Python through a structured 6-week roadmap.
