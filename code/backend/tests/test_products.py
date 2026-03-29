"""产品CRUD API测试"""

import pytest
from fastapi.testclient import TestClient


class TestProductAPI:
    """产品API测试类"""

    def test_create_product(self, client, sample_product_data):
        """测试创建产品"""
        response = client.post("/products/", json=sample_product_data)
        assert response.status_code == 201
        data = response.json()
        assert data["product_code"] == sample_product_data["product_code"]
        assert data["name"] == sample_product_data["name"]
        assert "id" in data

    def test_create_product_duplicate_code(self, client, sample_product_data):
        """测试创建重复产品编号应失败"""
        client.post("/products/", json=sample_product_data)
        response = client.post("/products/", json=sample_product_data)
        assert response.status_code == 400

    def test_list_products_empty(self, client):
        """测试空产品列表"""
        response = client.get("/products/")
        assert response.status_code == 200
        assert response.json() == []

    def test_list_products_with_data(self, client, sample_product_data):
        """测试有数据的产品列表"""
        client.post("/products/", json=sample_product_data)
        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["product_code"] == sample_product_data["product_code"]

    def test_get_product_by_id(self, client, sample_product_data):
        """测试根据ID获取产品"""
        create_response = client.post("/products/", json=sample_product_data)
        product_id = create_response.json()["id"]

        response = client.get(f"/products/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == sample_product_data["name"]

    def test_get_product_not_found(self, client):
        """测试获取不存在的产品"""
        response = client.get("/products/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404

    def test_update_product(self, client, sample_product_data):
        """测试更新产品"""
        create_response = client.post("/products/", json=sample_product_data)
        product_id = create_response.json()["id"]

        update_data = {"name": "Updated Product Name"}
        response = client.put(f"/products/{product_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Product Name"

    def test_delete_product(self, client, sample_product_data):
        """测试删除产品"""
        create_response = client.post("/products/", json=sample_product_data)
        product_id = create_response.json()["id"]

        response = client.delete(f"/products/{product_id}")
        assert response.status_code == 204

        # 验证已删除
        get_response = client.get(f"/products/{product_id}")
        assert get_response.status_code == 404


class TestProductValidation:
    """产品数据验证测试"""

    def test_create_product_missing_required_field(self, client):
        """测试缺少必填字段应失败"""
        incomplete_data = {"description": "Missing name and code"}
        response = client.post("/products/", json=incomplete_data)
        assert response.status_code == 422

    def test_create_product_invalid_status(self, client):
        """测试无效状态值"""
        data = {
            "product_code": "TEST-003",
            "name": "Test Product",
            "status": "invalid_status",
        }
        response = client.post("/products/", json=data)
        assert response.status_code == 422
