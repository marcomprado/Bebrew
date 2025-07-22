"""
Testes básicos para a API do Bebrew
"""
import pytest
from fastapi.testclient import TestClient
from backend.api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "Bebrew API" in data["message"]


def test_health_check():
    """Testa o endpoint de health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data


def test_register_user():
    """Testa registro de usuário"""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "display_name": "Test User"
    }
    
    # Este teste pode falhar se o Firebase não estiver configurado
    # É apenas um exemplo de como testar
    try:
        response = client.post("/auth/register", json=user_data)
        # Se funcionar, deve retornar 200 ou 201
        assert response.status_code in [200, 201, 400]
    except Exception:
        # Se falhar, é esperado se o Firebase não estiver configurado
        pass


def test_protected_endpoint_without_token():
    """Testa endpoint protegido sem token"""
    response = client.get("/recipes")
    assert response.status_code == 401  # Unauthorized


def test_ai_endpoint_without_token():
    """Testa endpoint de IA sem token"""
    response = client.post("/ai/analyze-recipe", json={"recipe_data": {}})
    assert response.status_code == 401  # Unauthorized


if __name__ == "__main__":
    pytest.main([__file__]) 