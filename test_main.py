from fastapi.testclient import TestClient
from main import app

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


def test_invalid_model_handling():
    """Testa se a API lida corretamente com um modelo inválido"""
    # Aqui você precisaria simular uma chamada que usa um modelo inválido.
    # Isso pode ser feito mockando a função chamar_gemini_blindado para lançar HTTPException.
    pass
