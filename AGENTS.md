# Agent 指南：ZOL 行情采集系统 (EFR 队)

## 1. 项目架构概述
- 本项目采用分层 OOP 架构：GUI (展现层) -> Main (调度层) -> Network/Spider (核心引擎)。
- 所有核心逻辑文件均位于 `code_python/` 目录下。

## 2. 核心模块职责
- `NetRequester`: 负责网络 I/O、自动重试与 SSL 绕过。禁止在此模块编写 HTML 解析逻辑。
- `DataParser`: 负责解析 DOM。必须通过 `config.py` 中的 Schema 驱动，禁止硬编码 CSS 选择器。

## 3. 编码规范约束
- **类型提示**: 新增函数必须包含 Python 类型标注（Type Hints）。
- **异常处理**: 禁止使用 `pass` 忽略错误，必须通过 `self.log` 或 `print` 输出异常上下文。
- **单元测试**: 任何对解析逻辑的修改，必须同步更新 `test_crawler.py` 并确保测试通过。

## 4. 禁止操作清单
- 未经许可禁止修改 `config.py` 中的现有字段名称。
- 禁止删除或修改 `.github/workflows/ci.yml` 自动化流水线配置。
- 禁止引入未经 `requirements.txt` 登记的第三方重度库。