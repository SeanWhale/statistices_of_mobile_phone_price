# config.py
import os

# 起点网址
BASE_URL = "https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1.html"

# 存储路径：自动创建 data 文件夹
OUTPUT_FILE = "phones_data_v2.csv"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://detail.zol.com.cn/"
}

MAX_RETRIES = 3
RETRY_DELAY = 2

# 提取规则：融合了第二版的“型号未知”等更细致的默认值
EXTRACTION_SCHEMA = {
    'container': 'li[data-follow-id]', 
    'fields': {
        'title': {'selector': 'h3 a', 'extract': 'text', 'default': '型号未知'},
        'price': {'selector': '.price-type', 'extract': 'text', 'clean': 'number', 'default': 0.0},
        'price_raw': {'selector': '.price-row', 'extract': 'text', 'default': '暂无报价'},
        'score': {'selector': '.score', 'extract': 'text', 'clean': 'number', 'default': 0.0},
        'comments': {'selector': '.comment-num', 'extract': 'text', 'pattern': r'(\d+)', 'clean': 'int', 'default': 0}
    }
}

PAGINATION = {'next_selector': 'a.next'}
