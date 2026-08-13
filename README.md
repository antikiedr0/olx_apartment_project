# Polish Housing Market Scraper & Analyzer

A data pipeline that scrapes, cleans, and stores apartment listings from the Polish real estate market for AI-powered analysis.

## Overview

This project collects apartment listings from **OLX** and **Otodom** — the two largest real estate platforms in Poland — across major Polish cities. The data is processed through an automated pipeline and stored in a PostgreSQL database, enabling market analysis and AI-based insights into pricing trends, availability, and property characteristics.
![Uploading image.png…]()

## Features

- Scrapes listings from OLX and Otodom across 8 major Polish cities
- Extracts key property attributes: price per m², area, number of rooms, floor, furnishing status, building type, and more
- Cleans and normalizes raw data (handles mixed formats, currency variants, encoding issues)
- Deduplicates listings across sources
- Stores structured data in PostgreSQL
- Orchestrated via a state machine for reliable end-to-end execution

## Pipeline

```
GET_OGLOSZENIA → GET_LINKS → SCRAPE_DATA → CLEAN_DATA → PUSH_TO_DB
```

1. **GET_OGLOSZENIA** — scrapes listing pages and saves titles, prices, and links
2. **GET_LINKS** — extracts individual listing URLs
3. **SCRAPE_DATA** — visits each listing and extracts detailed attributes
4. **CLEAN_DATA** — normalizes values, unifies key names, removes duplicates
5. **PUSH_TO_DB** — loads clean data into PostgreSQL

## Cities Covered

Warsaw, Gdansk, Krakow, Poznan, Wroclaw, Bydgoszcz, Szczecin, Lublin

## Tech Stack

- **Python** — scraping, data processing
- **BeautifulSoup** — HTML parsing
- **PostgreSQL** — data storage
- **Docker** — database container
- **psycopg2** — PostgreSQL driver

## Setup

```bash
# Start the database
docker compose up -d

# Install dependencies
pip install -r requirements.txt

# Run the full pipeline
python scraper/main.py
```
