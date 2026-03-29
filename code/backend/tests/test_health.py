"""健康检查API测试"""

from fastapi.testclient import TestClient


class TestHealthCheck:
    """健康检查API测试类"""

    def test_health_check_returns_200(self, client):
        """测试健康检查返回200状态码"""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_structure(self, client):
        """测试健康检查响应结构"""
        response = client.get("/health")
        data = response.json()

        assert "status" in data
        assert "database" in data
        assert "minio" in data
        assert "timestamp" in data

    def test_health_check_status_values(self, client):
        """测试健康检查状态值类型"""
        response = client.get("/health")
        data = response.json()

        assert isinstance(data["status"], str)
        assert isinstance(data["database"], bool)
        assert isinstance(data["minio"], bool)
        assert isinstance(data["timestamp"], str)

    def test_root_endpoint(self, client):
        """测试根路径返回API信息"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data or "status" in data
