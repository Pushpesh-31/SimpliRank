# Texas Tax Engine API

This project provides an API to calculate sales tax in Texas based on ZIP codes and generate filing data for jurisdictions. Includes an admin UI to update tax data from the Texas Comptroller.

## Features
- Calculate tax rate and total from address + amount
- Generate jurisdiction data for tax filing
- Admin UI to trigger latest tax data download

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Deployment
- Add to Railway, include this repo
- Railway uses Procfile to boot server

## Folder Structure
```
project/
├── main.py
├── tax_data/
│   ├── tx_rates.csv
│   └── download_latest.py
├── templates/
│   └── admin.html
├── requirements.txt
├── Procfile
└── README.md
```
