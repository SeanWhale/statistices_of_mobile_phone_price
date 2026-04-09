# network.py
import requests
import time
import urllib3

# 禁用安全警告（配合 verify=False）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class NetRequester:
    def __init__(self, headers, retries=3, delay=2):
        self.headers = headers
        self.retries = retries
        self.delay = delay

    def fetch(self, url):
        for i in range(self.retries):
            try:
                # 融合第二版的逻辑：显式指定编码
                response = requests.get(url, headers=self.headers, timeout=10, verify=False)
                response.raise_for_status()
                response.encoding = response.apparent_encoding or 'utf-8'
                return response.text
            except Exception as e:
                if i == self.retries - 1: return None
                time.sleep(self.delay)
        return None
