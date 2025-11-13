from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, RateLimitException

client = TestClient(app)


def test_health_check():
    """Testa se a rota /health responde 200 OK"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_root_redirect():
    """Testa se a raiz redireciona para o Swagger"""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"


@patch("main.chamar_gemini_blindado")
def test_simulacao_ia(mock_gemini):
    """Testa o endpoint de moderação simulando uma resposta da IA"""
    mock_gemini.return_value = {
        "aprovado": True,
        "motivo": None,
        "score_seguranca": 100,
    }

    payload = {"texto_usuario": "Eu amo programar em Python", "contexto": "bio"}

    response = client.post("/api/v1/seguranca/moderar", json=payload)

    assert response.status_code == 200
    assert response.json()["aprovado"] is True
    assert response.json()["score_seguranca"] == 100
