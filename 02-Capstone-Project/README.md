# Capstone Assignment 1 — E-Commerce Automation

**Technology:** Selenium WebDriver, Python, PyTest
**Website:** https://automationexercise.com

## Project Overview

This project is about automating an e-commerce website using Selenium WebDriver with Python and PyTest. It covers the product flow from login to checking the cart. There are four test cases, and they run in order using one Chrome browser.

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

## Test Cases

1. `test_01_login` — Login to the website. If the account does not exist, it signs up first.
2. `test_02_search_product` — Search for a product.
3. `test_03_add_product_and_update_quantity` — Clear the cart, set the quantity, and add the product.
4. `test_04_verify_cart_details` — Check the product name and quantity in the cart.

## Project Structure

```text id="c2q7wx"
02-Capstone-Project/
│
├── test_ecommerce.py     # Test cases
├── conftest.py           # Fixtures and screenshots
├── helpers.py            # Selenium functions
├── pytest.ini            # PyTest settings
├── test_data.json        # Test data
├── requirements.txt
├── README.md
├── screenshots/
└── reports/
```

## Setup

Install the required packages:

```bash id="5f3n9v"
pip install -r requirements.txt
```

## Run

```bash id="k6q4ww"
pytest
```

## Output

After execution:

* Screenshots are saved in `screenshots/`
* HTML report is saved in `reports/report.html`
