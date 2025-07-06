# 使用 Python 3.12 的官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 安装项目依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 将项目文件拷贝到容器中
COPY . /app

# 暴露应用端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

