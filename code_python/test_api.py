from fastapi.testclient import TestClient
from code_python.app import app
import pytest

# 创建测试客户端
client = TestClient(app)

def test_crawl_api_integration():
    """集成测试：验证 Web 接口能否完整走通抓取流程"""
    test_url = "https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1.html"
    
    # 模拟浏览器发送 GET 请求
    response = client.get(f"/api/crawl?url={test_url}")
    
    # 验证 1：状态码必须是 200
    assert response.status_code == 200
    
    # 验证 2：返回的数据格式必须正确
    json_data = response.json()
    assert json_data["status"] == "success"
    assert len(json_data["data"]) > 0
    assert "title" in json_data["data"][0]
    print(f"\n✅ 集成测试通过！成功抓取到 {len(json_data['data'])} 条数据。")