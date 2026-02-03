"""
Тесты для API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

from app.fastapi_main import app

client = TestClient(app)


class TestRootEndpoint:
    """Тесты для корневого endpoint"""
    
    def test_root_endpoint(self):
        """Тест корневого endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"
        

class TestHealthCheck:
    """Тесты для health check endpoint"""
    
    def test_health_check(self):
        """Тест проверки здоровья сервиса"""
        response = client.get("/api/v1/agent/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "AI Agent API"


class TestAgentQuery:
    """Тесты для agent query endpoint"""
    
    @patch('app.api.v1.agent.endpoints.run_multi_server_agent')
    def test_query_agent_success(self, mock_agent):
        """Тест успешного запроса к агенту"""
        # Мокаем ответ агента
        mock_agent.return_value = "Список продуктов: iPhone 15, MacBook Pro"
        
        response = client.post(
            "/api/v1/agent/query",
            json={"query": "Покажи все продукты"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "result" in data
        assert "iPhone" in data["result"]
        
    def test_query_agent_empty_query(self):
        """Тест с пустым запросом"""
        response = client.post(
            "/api/v1/agent/query",
            json={"query": ""}
        )
        
        # Должен вернуть ошибку валидации
        assert response.status_code == 422
        
    def test_query_agent_missing_query(self):
        """Тест без поля query"""
        response = client.post(
            "/api/v1/agent/query",
            json={}
        )
        
        # Должен вернуть ошибку валидации
        assert response.status_code == 422
        
    @patch('app.api.v1.agent.endpoints.run_multi_server_agent')
    def test_query_agent_value_error(self, mock_agent):
        """Тест обработки ValueError"""
        mock_agent.side_effect = ValueError("Продукт не найден")
        
        response = client.post(
            "/api/v1/agent/query",
            json={"query": "Найди продукт с ID 999"}
        )
        
        assert response.status_code == 400
        assert "Продукт не найден" in response.json()["detail"]
        
    @patch('app.api.v1.agent.endpoints.run_multi_server_agent')
    def test_query_agent_general_error(self, mock_agent):
        """Тест обработки общей ошибки"""
        mock_agent.side_effect = Exception("Внутренняя ошибка")
        
        response = client.post(
            "/api/v1/agent/query",
            json={"query": "Покажи продукты"}
        )
        
        assert response.status_code == 500
        

class TestAPIDocumentation:
    """Тесты для документации API"""
    
    def test_openapi_json(self):
        """Тест доступности OpenAPI спецификации"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        
    def test_swagger_ui(self):
        """Тест доступности Swagger UI"""
        response = client.get("/docs")
        assert response.status_code == 200
        
    def test_redoc(self):
        """Тест доступности ReDoc"""
        response = client.get("/redoc")
        assert response.status_code == 200
