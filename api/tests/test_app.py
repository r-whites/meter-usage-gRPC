import random
import pytest
from jsonschema import validate
from api.app import app

reading_schema = {
    "type": "object",
    "properties": {
        "time": { "type": "string", "format": "date-time" },
        "usage": { "type": "number" }
    }
}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_readings_n(client):
    N = random.randint(1, 3000)
    endpoint = f"/api/readings?n={N}"
    response = client.get(endpoint)
    assert len(response.json) == N


def test_readings_schema(client):
    N = 1
    endpoint = f"/api/readings?n={N}"
    response = client.get(endpoint)
    validate(instance=response.json[0], schema=reading_schema)

