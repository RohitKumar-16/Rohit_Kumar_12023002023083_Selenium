import os
import json
import time
import logging
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoAlertPresentException,
    NoSuchElementException,
    ElementClickInterceptedException,
)
from webdriver_manager.chrome import ChromeDriverManager

# Paths / constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
TEST_DATA_JSON = os.path.join(BASE_DIR, "test_data.json")
TEST_DATA_XLSX = os.path.join(BASE_DIR, "test_data.xlsx")  # optional
WAIT_TIMEOUT = 15

os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(REPORT_DIR, "execution.log")),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger("ecommerce_automation")

# Collects one dict per test step for the final HTML report
REPORT_RESULTS = []


# 8. Read test data from Excel/JSON
def load_test_data():
    if os.path.exists(TEST_DATA_XLSX):
        return _load_from_excel(TEST_DATA_XLSX)
    return _load_from_json(TEST_DATA_JSON)


def _load_from_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    log.info("Loaded test data from JSON: %s", path)
    return data


def _load_from_excel(path):
    from openpyxl import load_workbook

    wb = load_workbook(path)
    ws = wb.active
    headers = [c.value for c in ws[1]]
    row = [c.value for c in ws[2]]
    record = dict(zip(headers, row))

    data = {
        "base_url": record["base_url"],
        "login": {
            "email": record["email"],
            "password": record["password"],
            "name": record["name"],
        },
        "search": {
            "product_search_term": record["product_search_term"],
            "product_name_to_add": record["product_name_to_add"],
            "quantity": int(record["quantity"]),
        },
    }
    log.info("Loaded test data from Excel: %s", path)
    return data


# 7. Capture screenshots + step/report logging helpers
def record_step(driver, step_name, status="PASS", message=""):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = step_name.replace(" ", "_").lower()
    filename = f"{safe_name}_{timestamp}.png"
    filepath = os.path.join(SCREENSHOT_DIR, filename)

    try:
        driver.save_screenshot(filepath)
    except Exception as exc:  # noqa: BLE001 - screenshot failure shouldn't crash the run
        log.warning("Could not capture screenshot for %s: %s", step_name, exc)
        filename = None

    entry = {
        "step": step_name,
        "status": status,
        "message": message,
        "screenshot": filename,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    REPORT_RESULTS.append(entry)

    log_fn = log.info if status == "PASS" else log.error
    log_fn("[%s] %s - %s", status, step_name, message)


# 9. Handle popups / alerts
def dismiss_browser_alert_if_present(driver, accept=True):
    try:
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        text = alert.text
        alert.accept() if accept else alert.dismiss()
        log.info("Handled a browser alert: '%s'", text)
        return text
    except (TimeoutException, NoAlertPresentException):
        return None


def safe_click(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    time.sleep(0.3)  # let any sticky/animated overlay finish moving
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


def close_add_to_cart_modal(driver):
    try:
        continue_btn = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue Shopping']"))
        )
        safe_click(driver, continue_btn)
        log.info("Dismissed 'Added to cart' modal.")
    except TimeoutException:
        # Modal didn't appear - not fatal, continue the flow.
        log.info("No 'Added to cart' modal appeared.")


# 1. Launch browser
def launch_browser(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(2)
    return driver


# 2. Login to application (falls back to signup if the account doesn't exist)
def login_or_signup(driver, data, wait):
    login = data["login"]
    driver.get(f"{data['base_url']}/login")
    record_step(driver, "Open login page")

    email_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = driver.find_element(By.NAME, "password")
    # There are two forms on this page (signup + login), so scope the
    # login button via its data-qa attribute rather than a bare tag/class.
    login_btn = driver.find_element(By.CSS_SELECTOR, "button[data-qa='login-button']")

    email_field.clear()
    email_field.send_keys(login["email"])
    password_field.clear()
    password_field.send_keys(login["password"])
    safe_click(driver, login_btn)

    # Give the page a moment to redirect or show an error.
    time.sleep(1.5)

    error_visible = driver.find_elements(
        By.XPATH, "//p[contains(text(), 'incorrect') or contains(text(), 'Incorrect')]"
    )

    if error_visible:
        log.info("No existing account for this test email - signing up instead.")
        record_step(driver, "Login attempt", status="FAIL",
                    message="Account not found, switching to signup flow")
        _signup_new_account(driver, login, wait)
    else:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(., 'Logged in as')]")))
        record_step(driver, "Login", message=f"Logged in as {login['email']}")


def _signup_new_account(driver, login, wait):
    name_field = driver.find_element(By.NAME, "name")
    signup_email_field = driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']")
    name_field.clear()
    name_field.send_keys(login["name"])
    signup_email_field.clear()
    signup_email_field.send_keys(login["email"])
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, "button[data-qa='signup-button']"))

    password_field = wait.until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys(login["password"])

    driver.find_element(By.ID, "days").send_keys("1")
    driver.find_element(By.ID, "months").send_keys("January")
    driver.find_element(By.ID, "years").send_keys("2000")
    driver.find_element(By.ID, "first_name").send_keys(login["name"].split(" ")[0])
    driver.find_element(By.ID, "last_name").send_keys(
        login["name"].split(" ")[-1] if " " in login["name"] else "User"
    )
    driver.find_element(By.ID, "address1").send_keys("221B Test Street")
    driver.find_element(By.ID, "state").send_keys("West Bengal")
    driver.find_element(By.ID, "city").send_keys("Kolkata")
    driver.find_element(By.ID, "zipcode").send_keys("700001")
    driver.find_element(By.ID, "mobile_number").send_keys("9876543210")

    safe_click(driver, driver.find_element(By.CSS_SELECTOR, "button[data-qa='create-account']"))

    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "a[data-qa='continue-button']")))
    record_step(driver, "Signup", message=f"Account created for {login['email']}")
    safe_click(driver, driver.find_element(By.CSS_SELECTOR, "a[data-qa='continue-button']"))

    wait.until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(., 'Logged in as')]")))
    record_step(driver, "Login after signup", message=f"Logged in as {login['email']}")


# 3. Search product
def search_product(driver, search_term, wait):
    driver.get(f"{driver.current_url.split('/login')[0]}")  # no-op safeguard, kept explicit below
    base_url = driver.current_url.split("/", 3)
    driver.get("https://automationexercise.com/products")

    search_box = wait.until(EC.presence_of_element_located((By.ID, "search_product")))
    search_box.clear()
    search_box.send_keys(search_term)
    safe_click(driver, driver.find_element(By.ID, "submit_search"))

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "features_items")))
    results = driver.find_elements(By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    record_step(driver, "Search product", message=f"'{search_term}' returned {len(results)} result(s)")
    return results


# 4 & 5. Add product to cart + update quantity
def add_product_with_quantity(driver, product_name, quantity, wait):
    product_link = driver.find_element(
        By.XPATH, f"//p[text()='{product_name}']/ancestor::div[@class='product-image-wrapper']"
                  f"//a[contains(text(), 'View Product')]"
    )
    safe_click(driver, product_link)

    wait.until(EC.presence_of_element_located((By.ID, "quantity")))
    record_step(driver, "Open product details", message=product_name)

    qty_field = driver.find_element(By.ID, "quantity")
    qty_field.clear()
    qty_field.send_keys(str(quantity))
    record_step(driver, "Update quantity", message=f"Set quantity to {quantity}")

    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, "button.cart")
    safe_click(driver, add_to_cart_btn)

    dismiss_browser_alert_if_present(driver)  # in case any native alert fires
    close_add_to_cart_modal(driver)
    record_step(driver, "Add product to cart", message=f"{product_name} x{quantity}")


# 6. Verify cart details
def verify_cart(driver, product_name, expected_quantity, wait):
    driver.get("https://automationexercise.com/view_cart")
    wait.until(EC.presence_of_element_located((By.ID, "cart_info_table")))

    row = driver.find_element(
        By.XPATH, f"//tbody/tr[td[@class='cart_description']//a[text()='{product_name}']]"
    )
    quantity_text = row.find_element(By.CSS_SELECTOR, ".cart_quantity button").text.strip()

    if quantity_text == str(expected_quantity):
        record_step(
            driver, "Verify cart details",
            message=f"'{product_name}' present with correct quantity ({quantity_text})",
        )
        return True
    else:
        record_step(
            driver, "Verify cart details", status="FAIL",
            message=f"Expected qty {expected_quantity}, found {quantity_text}",
        )
        return False


# 10. Generate execution report
def generate_html_report():
    passed = sum(1 for r in REPORT_RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in REPORT_RESULTS if r["status"] == "FAIL")

    rows_html = ""
    for r in REPORT_RESULTS:
        color = "#1a7f37" if r["status"] == "PASS" else "#c62828"
        screenshot_cell = (
            f'<img src="../screenshots/{r["screenshot"]}" width="160">'
            if r["screenshot"] else "—"
        )
        rows_html += f"""
        <tr>
          <td>{r['time']}</td>
          <td>{r['step']}</td>
          <td style="color:{color}; font-weight:600;">{r['status']}</td>
          <td>{r['message']}</td>
          <td>{screenshot_cell}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Execution Report - E-Commerce Automation</title>
<style>
  body {{ font-family: Arial, sans-serif; margin: 30px; color: #222; }}
  h1 {{ margin-bottom: 4px; }}
  .summary {{ margin-bottom: 20px; font-size: 15px; }}
  .summary span {{ margin-right: 20px; font-weight: 600; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; font-size: 13px; text-align: left; vertical-align: top; }}
  th {{ background: #f5f5f5; }}
</style>
</head>
<body>
  <h1>E-Commerce Automation - Execution Report</h1>
  <div class="summary">
    <span>Total steps: {len(REPORT_RESULTS)}</span>
    <span style="color:#1a7f37;">Passed: {passed}</span>
    <span style="color:#c62828;">Failed: {failed}</span>
    <span>Run time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</span>
  </div>
  <table>
    <tr><th>Timestamp</th><th>Step</th><th>Status</th><th>Details</th><th>Screenshot</th></tr>
    {rows_html}
  </table>
</body>
</html>"""

    report_path = os.path.join(REPORT_DIR, "execution_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)
    log.info("Execution report written to %s", report_path)
    return report_path


# Main flow
def run():
    data = load_test_data()
    driver = launch_browser(headless=False)
    wait = WebDriverWait(driver, WAIT_TIMEOUT)

    try:
        driver.get(data["base_url"])
        record_step(driver, "Launch browser", message=f"Opened {data['base_url']}")

        login_or_signup(driver, data, wait)

        results = search_product(driver, data["search"]["product_search_term"], wait)
        if not results:
            raise AssertionError("No search results returned - cannot continue.")

        add_product_with_quantity(
            driver,
            data["search"]["product_name_to_add"],
            data["search"]["quantity"],
            wait
        )

        verify_cart(
            driver,
            data["search"]["product_name_to_add"],
            data["search"]["quantity"],
            wait,
        )

    except Exception as exc:  # noqa: BLE001 - top-level safety net for the whole run
        record_step(driver, "Unhandled error", status="FAIL", message=str(exc))
        log.exception("Test run failed")

    finally:
        report_path = generate_html_report()
        driver.quit()
        print(f"\nExecution report: {report_path}")


if __name__ == "__main__":
    run()
