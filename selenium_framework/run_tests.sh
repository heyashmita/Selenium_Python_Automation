#!/usr/bin/env bash
# Convenience script to install deps and run the full suite with HTML reporting.

set -e

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Running Unittest suite (Login)"
python -m unittest tests.test_login_unittest -v

echo "==> Running PyTest suite (Product Search) with HTML report"
pytest tests/test_product_search_pytest.py -v --html=reports/html/report.html --self-contained-html

echo "==> Running full PyTest suite (everything under tests/)"
pytest -v

echo "==> Done. Open reports/html/report.html to view the report."
