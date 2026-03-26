# config.py:存放网页地址和变量名

# 爬虫的起点网址（中关村在线手机频道）
BASE_URL = "https://detail.zol.com.cn/cell_phone_index/subcate57_0_list_1.html"

# 存储的文件名
OUTPUT_FILE = "phones_data.csv"

# 浏览器伪装
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://detail.zol.com.cn/"
}

MAX_RETRIES = 3
RETRY_DELAY = 2

# 数据提取配置
EXTRACTION_SCHEMA = {
    # 只要是带有 data-follow-id 属性的 li 标签，通通抓回来
    'container': 'li[data-follow-id]', 

    'fields': {
        'title': {
            'selector': 'h3 a',
            'extract': 'text', # 改为提取文字，更稳
            'default': '未知型号'
        },
        'price': {
            'selector': '.price-type',
            'extract': 'text',
            'clean': 'number',
            'default': 0.0
        },
        'price_raw': {
            'selector': '.price-row', # 扩大范围
            'extract': 'text',
            'default': '暂无报价'
        },
        'score': {
            'selector': '.score',
            'extract': 'text',
            'clean': 'number',
            'default': 0.0
        },
        'comments': {
            'selector': '.comment-num',
            'extract': 'text',
            'pattern': r'(\d+)',
            'clean': 'int',
            'default': 0
        }
    }
}

# 翻页配置
PAGINATION = {
    'next_selector': 'a.next', 
}
