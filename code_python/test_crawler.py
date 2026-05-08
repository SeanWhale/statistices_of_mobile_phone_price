# test_crawler.py
import pytest
from spider import DataParser
from network import NetRequester

# 模拟一段 ZOL 的 HTML 样本
SAMPLE_HTML = """
<li data-follow-id="123">
    <h3><a title="测试手机A">测试手机A</a></h3>
    <span class="price-type">5999</span>
    <span class="score">9.8</span>
</li>
"""

# 测试 1：验证 Schema 驱动的标题提取
def test_title_extraction():
    schema = {
        'container': 'li[data-follow-id]',
        'fields': {'title': {'selector': 'h3 a', 'extract': 'text', 'default': 'N/A'}}
    }
    parser = DataParser(schema)
    result = parser.parse(SAMPLE_HTML)
    assert result[0]['title'] == "测试手机A"

# 测试 2：验证价格数字清洗功能
def test_price_cleaning():
    schema = {
        'container': 'li',
        'fields': {'price': {'selector': '.price-type', 'extract': 'text', 'clean': 'number'}}
    }
    parser = DataParser(schema)
    result = parser.parse(SAMPLE_HTML)
    assert isinstance(result[0]['price'], float)
    assert result[0]['price'] == 5999.0

# 测试 3：验证翻页 URL 补全逻辑
def test_url_join():
    parser = DataParser({})
    current = "https://zol.com.cn/list.html"
    relative = "page-2.html"
    # 这里假设你 spider.py 里有 get_next_url 逻辑
    from urllib.parse import urljoin
    assert urljoin(current, relative) == "https://zol.com.cn/page-2.html"