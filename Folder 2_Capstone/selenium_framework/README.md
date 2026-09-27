# Selenium Python Automation Framework
### Unittest + PyTest + POM | Login & Product Search on automationexercise.com

## Demo Video
Full project walkthrough: [Watch here](https://drive.google.com/file/d/1Azg8AZg4owPFcx2uAR2bE-udddH3LxjQ/view?usp=sharing)

## 1. Project Structure

```
selenium_framework/
├── config/
│   └── config.ini              # Environment, browser, timeout & path settings
├── pages/                      # Page Object Model
│   ├── base_page.py            # Common wait/click/type wrappers used by every page
│   ├── login_page.py           # Login / Signup page
│   ├── home_page.py            # Home page
│   └── product_search_page.py  # Products / search page
├── utils/                      # Utility / helper classes
│   ├── config_reader.py        # Reads config.ini, allows env-var overrides
│   ├── driver_factory.py       # Creates Chrome/Firefox/Edge WebDriver instances
│   ├── csv_reader.py           # Loads CSV test data as dicts/tuples
│   ├── screenshot_util.py      # Captures screenshots (used on failure)
│   └── logger.py               # Shared logger -> reports/execution.log
├── testdata/
│   ├── login_data.csv          # Data-driven login scenarios
│   └── search_data.csv         # Data-driven search terms
├── tests/
│   ├── test_login_unittest.py       # Login suite (unittest)
│   └── test_product_search_pytest.py# Search suite (pytest, parametrized)
├── reports/
│   ├── html/                   # pytest-html reports land here
│   └── screenshots/            # Failure screenshots land here
├── conftest.py                 # PyTest fixtures + auto screenshot-on-failure hook
├── pytest.ini                  # PyTest configuration
├── requirements.txt
└── run_tests.sh                # One-shot install + run + report script
```

## 2. Design Highlights

- **Page Object Model (POM):** Every page has its own class under `pages/`,
  extending `BasePage`, which centralizes explicit waits, clicks, typing, and
  visibility checks. Tests never call Selenium APIs directly.
- **Config Management:** `config/config.ini` holds base URL, browser, headless
  flag, and timeouts. `ConfigReader` exposes typed getters and lets you override
  `BROWSER` / `HEADLESS` via environment variables without touching the file,
  e.g. `HEADLESS=true BROWSER=chrome pytest`.
- **Test Data Handling (CSV):** `utils/csv_reader.py` loads
  `testdata/login_data.csv` and `testdata/search_data.csv`. The PyTest suite
  turns CSV rows directly into `pytest.mark.parametrize` cases; the Unittest
  suite loops over rows using `subTest`.
- **Screenshots on Failure:**
  - PyTest: `conftest.py` implements `pytest_runtest_makereport`, which fires
    after every test call, and captures + embeds a screenshot into the HTML
    report whenever a test using the `driver` fixture fails.
  - Unittest: `TestLoginUnittest.tearDown()` inspects `self._outcome.result`
    and captures a screenshot when the current test failed/errored.
- **HTML Reporting:** `pytest-html` is pre-wired via `pytest.ini`
  (`addopts = --html=reports/html/report.html --self-contained-html`), so
  every `pytest` run produces a single self-contained HTML report with
  embedded failure screenshots.
- **Two runner styles in one framework:** `test_login_unittest.py` is a pure
  `unittest.TestCase` (runnable with `python -m unittest`), while
  `test_product_search_pytest.py` uses PyTest fixtures/parametrize — both are
  also collected and run together by plain `pytest`, satisfying the
  "Unittest + PyTest" requirement in a single codebase.

## 3. Setup

```bash
cd selenium_framework
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Chrome/Firefox/Edge binaries must be installed on the machine; `webdriver-manager`
downloads the matching driver binary automatically the first time a browser
session starts.

## 4. Configuration

Edit `config/config.ini`:

```ini
[ENVIRONMENT]
base_url = https://automationexercise.com
browser = chrome        ; chrome | firefox | edge
headless = false
implicit_wait = 10
explicit_wait = 15
page_load_timeout = 30
```

Override at runtime without editing the file:
```bash
HEADLESS=true BROWSER=firefox pytest
```

## 5. Running Tests

Run everything (unittest tests are auto-discovered by pytest too):
```bash
pytest
```

Run only the Unittest login suite, the unittest way:
```bash
python -m unittest tests.test_login_unittest -v
```

Run only the PyTest product-search suite:
```bash
pytest tests/test_product_search_pytest.py -v
```

Run by marker (defined in `pytest.ini`):
```bash
pytest -m smoke
pytest -m "search and regression"
```

Generate/regenerate the HTML report explicitly:
```bash
pytest --html=reports/html/report.html --self-contained-html
```

Or simply:
```bash
./run_tests.sh
```

## 6. Test Data

`testdata/login_data.csv`:
| email | password | expected_result |
|---|---|---|
| valid_registered_user@example.com | ValidPass@123 | success |
| wronguser@example.com | WrongPass@123 | failure |
| not_an_email | SomePass123 | failure |
| valid_registered_user@example.com | WrongPassword1 | failure |

> **Note:** automationexercise.com requires a genuinely registered account for
> a *successful* login. Replace the `success` row's email/password with a real
> account you've created via the site's Signup flow (or automate registration
> first) before relying on that row; the framework treats all `failure` rows
> as the primary negative-path regression set, which need no pre-registration.

`testdata/search_data.csv`:
| search_term | expect_results |
|---|---|
| Dress | yes |
| Tshirt | yes |
| Jeans | yes |
| xyznotarealproductname | no |

Add rows to either file to extend coverage — no code changes required.

## 7. Reports & Artifacts

- HTML report: `reports/html/report.html` (self-contained, open in any browser)
- Failure screenshots: `reports/screenshots/<test_name>_<timestamp>.png`
- Execution log: `reports/execution.log`

## 8. Extending the Framework

- **New page:** create `pages/new_page.py` extending `BasePage`, define
  locators as class-level tuples, and add action/assertion methods.
- **New test data:** drop a new CSV into `testdata/`, read it with
  `CSVReader.read("file.csv")`.
- **New browser:** already supported — set `browser = firefox` or `edge` in
  `config.ini`; `DriverFactory` handles the rest via webdriver-manager.
- **CI integration:** the framework is headless-ready (`headless = true`) and
  exits with standard process codes, so it drops into any CI pipeline
  (GitHub Actions, Jenkins, GitLab CI) by simply running `pip install -r
  requirements.txt && pytest`.

