from helpers import (
    login_or_signup,
    is_logged_in,
    search_product,
    add_product_with_quantity,
    get_cart_quantity,
    clear_cart,
)


def test_01_login(driver, test_data):
    login_or_signup(driver, test_data)

    assert is_logged_in(driver), "'Logged in as ...' was not shown after login"


def test_02_search_product(driver, test_data):
    term = test_data["search"]["product_search_term"]

    results = search_product(driver, test_data["base_url"], term)

    assert len(results) > 0, f"No search results found for '{term}'"


def test_03_add_product_and_update_quantity(driver, test_data):
    search = test_data["search"]
    clear_cart(driver, test_data["base_url"])  # start every run with an empty cart
    search_product(driver, test_data["base_url"], search["product_search_term"])

    entered_quantity = add_product_with_quantity(
        driver, search["product_name_to_add"], search["quantity"]
    )

    assert entered_quantity == str(search["quantity"]), (
        f"Quantity field shows {entered_quantity}, expected {search['quantity']}"
    )


def test_04_verify_cart_details(driver, test_data):
    search = test_data["search"]

    cart_quantity = get_cart_quantity(
        driver, test_data["base_url"], search["product_name_to_add"]
    )

    assert cart_quantity is not None, (
        f"'{search['product_name_to_add']}' was not found in the cart"
    )
    assert cart_quantity == str(search["quantity"]), (
        f"Cart shows quantity {cart_quantity}, expected {search['quantity']}"
    )
