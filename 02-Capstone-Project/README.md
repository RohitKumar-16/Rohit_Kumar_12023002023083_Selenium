# Capstone Assignment 1 — E-Commerce Automation

**Technology:** Selenium WebDriver, Python
**Website:** https://automationexercise.com

## Project Overview

Automated an e-commerce website using Selenium WebDriver with Python. The project automates the complete product purchase flow from login to cart verification.

## Features

* Launch browser
* Login / Signup
* Search for a product
* Add product to cart
* Update product quantity
* Verify cart details
* Capture screenshots
* Read test data from JSON/Excel
* Handle alerts and popups
* Generate HTML execution report

## Project Structure

```text
ecommerce_automation/
│
├── ecommerce_automation.py
├── test_data.json
├── requirements.txt
├── README.md
├── screenshots/
└── reports/
```

## Setup

Install the required packages:

```bash
pip install -r requirements.txt
```

Make sure Google Chrome is installed.

## Run

```bash
python ecommerce_automation.py
```

After execution:

* Screenshots are saved in `screenshots/`
* Execution logs are saved in `reports/`
* HTML report is saved as `reports/execution_report.html`
