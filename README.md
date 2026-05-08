# statistices_of_mobile_phone_price
🚩 团队概览
#### 团队名称：EFR队
口号：蛋炒饭，越炒越香
#### 对应的成员角色分配：
产品负责人 (PO)：PCY  
Scrum Master (SM)：ZMY  
开发团队 (Dev Team)：LJX
### 项目简介
本项目是一个基于 面向对象 (OOP) 架构的电商行情自动化采集系统。通过解耦网络请求与解析逻辑，配合声明式规则配置，实现高效、稳健的数码产品价格监控。
技术栈：Python, Pandas, Matplotlib, Seaborn, Scikit-learn
核心库：requests, BeautifulSoup4, customtkinter (GUI), pytest (TDD)


1. 系统架构图 (Mermaid)
本系统采用分层架构设计，确保了 UI 展现层与核心抓取引擎的彻底解耦
graph TD
    User((用户/分析师)) --> GUI[gui.py - 现代图形界面]
    GUI --> Main[main.py - 调度指挥中心]
    Main --> Req[network.py - 网络引擎类]
    Main --> Parser[spider.py - 配置化解析类]
    Parser --> Config[config.py - 规则配置库]
    Main --> Storage[storage.py - 数据存储模块]
    Storage --> CSV[(phones_data.csv)]
    Req -- SSL请求 --> Server(ZOL 目标服务器)

2. 核心业务模块职责说明
NetRequester (network.py)：负责“网页下载”。包含浏览器伪装 (UA)、自动重试逻辑及 SSL 安全校验绕过。
DataParser (spider.py)：负责“内容翻译”。不关心网络环境，仅根据 config.py 中的 Schema 规则将 HTML 文档转换为结构化字典。
Config (config.py)：系统的“大脑”。集中管理爬取目标的 CSS 选择器、清洗正则及翻页逻辑。
Storage (storage.py)：负责“本地持久化”。处理 utf-8-sig 编码以确保生成的 CSV 文件在 Excel 中不乱码。

3. 本地开发环境搭建
第一步：克隆并导入依赖
打开终端执行以下命令：
# 导入依赖库
pip install -r requirements.txt
第二步：创建并激活环境
python -m venv .venv
# Windows 激活命令
.\.venv\Scripts\Activate.ps1
第三步：自动化测试验证 (TDD)
在运行前执行单元测试，确保解析引擎逻辑正常：
python -m pytest code_python/test_crawler.py
第四步：启动程序
# 启动图形化界面
python code_python/main.py --gui

4. 工程质量保证 (CI)
本项目已集成 GitHub Actions。每次代码推送 (Push) 或发起合并请求 (PR) 时，系统将自动触发：
环境依赖安装。
flake8 规范化校验。
pytest 单元测试运行。
确保主干分支始终保持 Green Build 状态。