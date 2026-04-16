# main.py
import sys
import config
import storage
import time
from network import NetRequester
from spider import DataParser
from tqdm import tqdm
from gui import CrawlerGUI

def run_cli():
    print("🚀 [命令行模式] 启动...")
    req = NetRequester(config.HEADERS)
    p = DataParser(config.EXTRACTION_SCHEMA)
    
    all_data = []
    max_pages = 5
    next_url = config.BASE_URL
    pbar = tqdm(total=max_pages, desc="🚚 采集进度", unit="页")
    
    for i in range(max_pages):
        if not next_url: break
        html = req.fetch(next_url)
        if not html: break
        
        items = p.parse(html)
        all_data.extend(items)
        pbar.update(1)
        next_url = p.get_next_url(html, next_url, config.PAGINATION['next_selector'])
        time.sleep(1.5)

    pbar.close()
    if all_data: storage.save_to_csv(all_data, config.OUTPUT_FILE)
    print(f"✨ 任务完成，共抓取 {len(all_data)} 条。")

def run_gui():
    print("🎨 [图形界面模式] 启动...")

    app = CrawlerGUI()
    app.mainloop()

if __name__ == "__main__":
    # 如果运行 python main.py --gui 则启动界面，否则跑终端
    if "--gui" in sys.argv:
        run_gui()
    else:
        run_cli()
