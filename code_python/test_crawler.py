# test_crawler.py (改进版 - 资深工程师/CoT 指令产出)
import pytest
import requests
from unittest.mock import patch, MagicMock
from code_python.spider import DataParser
from code_python.network import NetRequester

# ==========================================
# 1. DataParser 防御性提取测试 (覆盖所有 if/else)
# ==========================================
def test_parser_with_missing_elements():
    """模拟标签缺失、属性缺失，验证 Default 值逻辑"""
    schema = {
        'container': 'li',
        'fields': {
            'price': {'selector': '.non-exist', 'clean': 'number', 'default': 0.0},
            'link': {'selector': 'h3', 'extract': 'attr:href', 'default': 'no_link'}
        }
    }
    html = "<li><h3>没有链接的标题</h3></li>"
    parser = DataParser(schema)
    result = parser.parse(html)
    assert result[0]['price'] == 0.0
    assert result[0]['link'] == 'no_link'

def test_complex_price_cleaning():
    """验证重构后的高精度价格清洗逻辑 (5,999.50 -> 5999)"""
    html = '<li><span class="p"> $5,999.50 </span></li>'
    schema = {'container': 'li', 'fields': {'price': {'selector': '.p', 'clean': 'int'}}}
    parser = DataParser(schema)
    assert parser.parse(html)[0]['price'] == 5999

# ==========================================
# 2. NetRequester 异常重试测试 (Mock 驱动)
# ==========================================
def test_network_retry_logic():
    """演化目标：利用 Mock 模拟前两次超时，第三次成功的极限场景"""
    with patch('requests.get') as mock_get:
        # 定义模拟行为：抛出两个异常，然后返回一个成功的 Response
        mock_get.side_effect = [
            requests.exceptions.Timeout("超时"),
            requests.exceptions.ConnectionError("断开"),
            MagicMock(status_code=200, text="<html>Success</html>", apparent_encoding='utf-8')
        ]
        
        req = NetRequester(headers={}, retries=3, delay=0) # delay设为0秒出结果
        result = req.fetch("http://mock-test.com")
        
        # 断言：是否真的重试了 3 次
        assert mock_get.call_count == 3
        assert result == "<html>Success</html>"

def test_network_total_failure():
    """验证当 3 次机会全部耗尽后的处理"""
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException("服务器崩溃")
        req = NetRequester(headers={}, retries=3, delay=0)
        result = req.fetch("http://fail.com")
        
        assert result is None
        assert mock_get.call_count == 3

def test_url_join_logic():
    from urllib.parse import urljoin
    assert urljoin("https://zol.com.cn/", "page-2.html") == "https://zol.com.cn/page-2.html"
    
# 追加到 test_crawler.py 末尾
def test_spider_edge_cases():
    """专门为了冲破 80% 覆盖率补齐的边界测试"""
    parser = DataParser({'container': 'li', 'fields': {}})
    # 1. 测试 HTML 为空的情况 (覆盖 if not html 分支)
    assert parser.parse("") == []
    
    # 2. 测试 找不到容器的情况 (覆盖 if not containers 分支)
    assert parser.parse("<div>nothing</div>") == []

def test_pagination_logic():
    """测试翻页逻辑 (覆盖 get_next_url 函数)"""
    parser = DataParser({})
    html = '<a class="next" href="page-2.html">Next</a>'
    current_url = "https://zol.com.cn/list.html"
    
    # 正常找到下一页
    next_url = parser.get_next_url(html, current_url, "a.next")
    assert "page-2.html" in next_url
    
    # 找不到下一页
    assert parser.get_next_url("<div></div>", current_url, "a.next") is None