import pytest
@pytest.mark.asyncio
async def test_churn(client):
    r = await client.post("/api/accounts", json={"name": "Acme", "mrr": 900, "days_since_login": 45, "tickets_open": 4, "nps": 3})
    assert r.status_code == 200
    assert r.json()["band"] in {"high", "medium", "low"}
