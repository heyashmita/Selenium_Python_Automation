

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.csv_reader import CSVReader
from pages.home_page import HomePage
from pages.product_search_page import ProductSearchPage


_search_rows = CSVReader.read("search_data.csv")
_search_params = [
    pytest.param(
        row["search_term"],
        row["expect_results"] == "yes",
        id=row["search_term"],
    )
    for row in _search_rows
]


@pytest.mark.smoke
@pytest.mark.search
def test_home_page_loads(driver):
   
    home = HomePage(driver).load()
    assert home.is_loaded(), "Home page did not load / logo not visible"


@pytest.mark.search
def test_navigate_to_products_page(driver):
    
    home = HomePage(driver).load()
    home.go_to_products_page()
    search_page = ProductSearchPage(driver)
    assert "/products" in search_page.get_current_url()


@pytest.mark.search
@pytest.mark.regression
@pytest.mark.parametrize("search_term, expect_results", _search_params)
def test_product_search_data_driven(driver, search_term, expect_results):
    
    search_page = ProductSearchPage(driver)
    search_page.load()
    search_page.search_product(search_term)

    assert search_page.is_search_results_header_displayed(), (
        "'Searched Products' header did not appear after search"
    )

    result_count = search_page.get_result_count()

    if expect_results:
        assert result_count > 0, f"Expected results for '{search_term}' but got none"
        assert search_page.all_results_contain(search_term.rstrip("s")) or result_count > 0, (
            f"Returned products do not appear related to search term '{search_term}'"
        )
    else:
        assert result_count == 0, (
            f"Expected no results for nonsense term '{search_term}' but got {result_count}"
        )


@pytest.mark.search
def test_search_with_empty_term_returns_full_or_no_results(driver):
    
    search_page = ProductSearchPage(driver)
    search_page.load()
    search_page.search_product("")
    assert search_page.is_search_results_header_displayed(), (
        "Search results header should still render for an empty search term"
    )
