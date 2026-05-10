# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt fastapi uvicorn

# 拷贝代码
COPY . .

# 暴露 FastAPI 默认端口
EXPOSE 8000

# 运行 Web 服务器
CMD ["uvicorn", "code_python.app:app", "--host", "0.0.0.0", "--port", "8000"]