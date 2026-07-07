from fastapi.testclient import TestClient
from filinglens.api.routes import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
client = TestClient(app)

def test_agent_api_ask():
    response = client.post("/agent-ask", json={"question": "Test", "debug": True})
    assert response.status_code == 200
    data = response.json()
    assert "execution_trace" in data
    assert "planner" in data
