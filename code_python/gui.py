# gui.py
import customtkinter as ctk
import threading  # 👈 关键：防止界面在爬取时卡死
import config
from network import NetRequester
from spider import DataParser
import storage
import time

# 设置主题
ctk.set_appearance_mode("dark")  # 也可以是 "light"
ctk.set_default_color_theme("blue")

class CrawlerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ZOL 智能行情采集系统 v1.0")
        self.geometry("600x450")

        # --- 1. 标题 ---
        self.label = ctk.CTkLabel(self, text="数码产品价格自动化采集工具", font=("微软雅黑", 24, "bold"))
        self.label.pack(pady=20)

        # --- 2. 输入区域 ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=10, padx=20, fill="x")

        self.url_label = ctk.CTkLabel(self.input_frame, text="起始网址:")
        self.url_label.grid(row=0, column=0, padx=10, pady=10)
        self.url_entry = ctk.CTkEntry(self.input_frame, width=350)
        self.url_entry.insert(0, config.BASE_URL)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)

        # --- 3. 进度条 ---
        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=20)

        # --- 4. 日志显示区 ---
        self.textbox = ctk.CTkTextbox(self, width=500, height=150)
        self.textbox.pack(pady=10)

        # --- 5. 按钮 ---
        self.start_button = ctk.CTkButton(self, text="开始同步抓取", command=self.start_thread)
        self.start_button.pack(pady=20)

    def log(self, message):
        """在界面文本框打印日志"""
        self.textbox.insert("end", f"{message}\n")
        self.textbox.see("end")

    def start_thread(self):
        """点击按钮后开启新线程，防止界面卡死"""
        self.start_button.configure(state="disabled")
        self.textbox.delete("0.0", "end")
        # 开启后台线程执行爬虫
        t = threading.Thread(target=self.run_crawler)
        t.start()

    def run_crawler(self):
        """核心爬取逻辑 (从 main.py 移植过来)"""
        try:
            self.log("🚀 引擎初始化中...")
            requester = NetRequester(config.HEADERS)
            parser = DataParser(config.EXTRACTION_SCHEMA)
            
            all_data = []
            max_pages = 5
            next_url = self.url_entry.get()
            
            for page in range(1, max_pages + 1):
                if not next_url: break
                
                self.log(f"🕵️ 正在采集第 {page} 页...")
                html = requester.fetch(next_url)
                if not html: break
                
                items = parser.parse(html)
                all_data.extend(items)
                
                # 更新进度条和日志
                self.progress_bar.set(page / max_pages)
                self.log(f"✅ 成功提取 {len(items)} 条，累计 {len(all_data)} 条")
                
                next_url = parser.get_next_url(html, next_url, config.PAGINATION['next_selector'])
                time.sleep(1)

            if all_data:
                storage.save_to_csv(all_data, config.OUTPUT_FILE)
                self.log(f"\n✨ 任务圆满完成！数据已保存。")
            
        except Exception as e:
            self.log(f"❌ 运行报错: {e}")
        finally:
            self.start_button.configure(state="normal")

if __name__ == "__main__":
    app = CrawlerGUI()
    app.mainloop()
