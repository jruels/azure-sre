import requests
import time
from log_analytics import send_log_to_loganalytics

BASE_URL = "https://finapi-yourname.azurewebsites.net" #  <------ Replace with your actual base URL
logs = []

def log_result(name, status, url, method, duration, status_code, message=""):
    logs.append({
        "test": name,
        "status": status,
        "url": url,
        "method": method,
        "duration_seconds": round(duration, 3),
        "status_code": status_code,
        "message": message,
        "source": "smoke-tests.yml"
    })

def run_test(name, method, url, check_fn):
    start = time.time()
    try:
        response = requests.request(method, url, timeout=5)
        duration = time.time() - start
        check_fn(response)
        log_result(name, "pass", url, method, duration, response.status_code)
    except Exception as e:
        duration = time.time() - start
        status_code = response.status_code if 'response' in locals() else 0
        log_result(name, "fail", url, method, duration, status_code, str(e))
        raise

# ----- Actual tests below -----

def test_home():
    run_test(
        name="test_home",
        method="GET",
        url=f"{BASE_URL}/",
        check_fn=lambda r: (
            assert_status(r, 200),
            assert_in_text(r, "Flask")
        )
    )

def test_retrieve_price():
    run_test(
        name="test_retrieve_price",
        method="GET",
        url=f"{BASE_URL}/api/retrieve-price?symbol=AAPL",
        check_fn=lambda r: (
            assert_status(r, 200),
            assert_equal(r.json().get("symbol"), "AAPL")
        )
    )

def test_client_valuation():
    run_test(
        name="test_client_valuation",
        method="GET",
        url=f"{BASE_URL}/api/client-valuation",
        check_fn=lambda r: (
            assert_status(r, 200),
            assert_is_instance(r.json(), list)
        )
    )

def test_get_portfolio():
    run_test(
        name="test_get_portfolio",
        method="GET",
        url=f"{BASE_URL}/api/portfolio/P001",
        check_fn=lambda r: (
            assert_status(r, 200),
            assert_equal(r.json().get("PortfolioID"), "P001")
        )
    )

def test_list_reports():
    run_test(
        name="test_list_reports",
        method="GET",
        url=f"{BASE_URL}/api/list-reports",
        check_fn=lambda r: (
            assert_in(r.status_code, [200, 500])
        )
    )

def test_slow_endpoint():
    run_test(
        name="test_slow_endpoint",
        method="GET",
        url=f"{BASE_URL}/api/slow-endpoint",
        check_fn=lambda r: (
            assert_status(r, 200)
        )
    )

# ----- Assertion helpers -----

def assert_status(response, expected):
    assert response.status_code == expected, f"Expected {expected}, got {response.status_code}"

def assert_equal(actual, expected):
    assert actual == expected, f"Expected {expected}, got {actual}"

def assert_is_instance(obj, typ):
    assert isinstance(obj, typ), f"Expected type {typ}, got {type(obj)}"

def assert_in_text(response, text):
    assert text in response.text, f"'{text}' not found in response body"

def assert_in(value, options):
    assert value in options, f"{value} not in allowed values: {options}"

# ----- Final hook to send logs -----

def test_send_logs_to_log_analytics():
    print("Sending smoke test logs to Log Analytics (from final test)...")
    if logs:
        print(f"Total logs to send: {len(logs)}")
        send_log_to_loganalytics("SmokeTestResults", logs)
    else:
        print("⚠️ No logs collected.")

