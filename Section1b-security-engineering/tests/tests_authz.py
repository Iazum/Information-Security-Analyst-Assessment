import httpx
BASE = "http://localhost:8000"

def test_user_a_cannot_read_user_b_order():
    r = httpx.get(f"{BASE}/api/orders/2", headers={"Authorization": "Bearer token-a"})
    assert r.status_code in (403, 404)   # FAILS on your vulnerable app
