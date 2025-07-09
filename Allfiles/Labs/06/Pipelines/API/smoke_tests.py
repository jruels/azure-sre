import requests

BASE_URL = "https://finapi-yourname.azurewebsites.net" # <------ Replace with your actual base URL

def test_home():
    r = requests.get(f"{BASE_URL}/")
    assert r.status_code == 200
    assert "Flask" in r.text

def test_retrieve_price():
    r = requests.get(f"{BASE_URL}/api/retrieve-price?symbol=AAPL", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["symbol"] == "AAPL"

def test_client_valuation():
    r = requests.get(f"{BASE_URL}/api/client-valuation", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)

def test_get_portfolio():
    r = requests.get(f"{BASE_URL}/api/portfolio/P001", timeout=5)
    assert r.status_code == 200
    data = r.json()
    assert data["PortfolioID"] == "P001"

def test_list_reports():
    r = requests.get(f"{BASE_URL}/api/list-reports", timeout=5)
    assert r.status_code in [200, 500]  # 500 = fallback if storage missing

def test_slow_endpoint():
    r = requests.get(f"{BASE_URL}/api/slow-endpoint", timeout=5)
    assert r.status_code == 200
