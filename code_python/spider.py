# spider.py
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

class DataParser:
    def __init__(self, schema):
        self.schema = schema

    def parse(self, html):
        if not html: return []
        soup = BeautifulSoup(html, "html.parser")
        containers = soup.select(self.schema['container'])
        
        results = []
        for container in containers:
            item = {}
            for f_name, f_rule in self.schema['fields'].items():
                item[f_name] = self._extract_field(container, f_rule)
            results.append(item)
        return results

    def _extract_field(self, container, rule):
        elem = container.select_one(rule.get('selector'))
        if not elem: return rule.get('default')

        extract_type = rule.get('extract', 'text')
        raw_value = elem.get(extract_type.split(':')[1]) if extract_type.startswith('attr:') else elem.get_text(strip=True)
        
        if not raw_value: return rule.get('default')

        if 'pattern' in rule:
            match = re.search(rule['pattern'], str(raw_value))
            if match: raw_value = match.group(1)
        
        clean_type = rule.get('clean')
        
        # --- 核心修正逻辑开始 ---
        if clean_type in ['number', 'int']:
            # 1. 先去掉千分位逗号 (例如 5,999.00 -> 5999.00)
            cleaned = str(raw_value).replace(',', '')
            # 2. 正则保留：数字、小数点、负号。去掉其它所有杂质 (如 $ ￥)
            cleaned = re.sub(r'[^\d.-]', '', cleaned)
            
            if not cleaned or cleaned == '.': return rule.get('default')
            
            try:
                val_float = float(cleaned)
                return int(val_float) if clean_type == 'int' else val_float
            except (ValueError, TypeError):
                return rule.get('default')
        # --- 核心修正逻辑结束 ---
        
        return raw_value

    def get_next_url(self, html, current_url, next_selector):
        if not html: return None
        soup = BeautifulSoup(html, "html.parser")
        next_btn = soup.select_one(next_selector)
        if next_btn and next_btn.has_attr('href'):
            return urljoin(current_url, next_btn['href'])
        return None