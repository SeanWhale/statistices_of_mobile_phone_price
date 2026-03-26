# spider.py:负责网页请求和数据解析
import requests
from bs4 import BeautifulSoup
import re
import time
import config
from urllib.parse import urljoin

def get_html(url):
    for attempt in range(1, config.MAX_RETRIES + 1):
        try:
            response = requests.get(url, headers=config.HEADERS, timeout=10)
            response.raise_for_status()
            response.encoding = response.apparent_encoding or 'utf-8'
            return response.text
        except Exception as e:
            if attempt == config.MAX_RETRIES:
                print(f"❌ 最终失败: {e}")
                return None
            time.sleep(config.RETRY_DELAY)
    return None

def parse_books(html):
    if not html: return []
   
    soup = BeautifulSoup(html, "html.parser")
    schema = config.EXTRACTION_SCHEMA
    containers = soup.select(schema['container'])
    
    # 调试信息：如果没找到容器，打印出来
    if not containers:
        print(f"⚠️ 未找到容器: {schema['container']}。可能是网站改版或选择器错误。")
        return []

    results = []
    for container in containers:
        item = {}
        for field_name, field_rule in schema['fields'].items():
            item[field_name] = _extract_field(container, field_rule)
        results.append(item)
    return results

def _extract_field(container, rule):
    selector = rule.get('selector')
    extract_type = rule.get('extract', 'text')
    default = rule.get('default')

    elem = container.select_one(selector)
    if not elem: return default

    if extract_type == 'text':
        raw_value = elem.get_text(strip=True)
    elif extract_type.startswith('attr:'):
        attr_name = extract_type.split(':', 1)[1]
        raw_value = elem.get(attr_name)
    else:
        raw_value = elem.get_text(strip=True)

    if raw_value is None: return default

    if 'pattern' in rule:
        match = re.search(rule['pattern'], raw_value)
        if match: raw_value = match.group(1)
    
    clean_type = rule.get('clean')
    if clean_type == 'number':
        cleaned = re.sub(r'[^\d.]', '', str(raw_value))
        return float(cleaned) if cleaned else default
    elif clean_type == 'int':
        cleaned = re.sub(r'[^\d]', '', str(raw_value))
        return int(cleaned) if cleaned else default

    return raw_value

def get_next_page_url(html, current_url):
    if not html: return None
    soup = BeautifulSoup(html, "html.parser")
    next_selector = config.PAGINATION.get('next_selector', 'a.next')
    next_btn = soup.select_one(next_selector)
    if next_btn and next_btn.has_attr('href'):
        return urljoin(current_url, next_btn['href'])
    return None
