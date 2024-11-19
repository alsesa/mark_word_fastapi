# 使用 Python 3.12 的官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 将项目文件拷贝到容器中
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露应用端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

