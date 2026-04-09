# storage.py
import csv
import os

def save_to_csv(data, filename):
    if not data: return False
    try:
        # 自动创建目录
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            field_map = {'title': '型号', 'price': '价格', 'price_raw': '原始价格', 'score': '评分', 'comments': '评价人数'}
            writer = csv.DictWriter(f, fieldnames=field_map.keys())
            # 写入自定义中文表头
            f.write("型号,价格,原始价格,评分,评价人数\n")
            writer.writerows(data)
        return True
    except Exception as e:
        print(f"❌ 存储失败: {e}")
        return False
