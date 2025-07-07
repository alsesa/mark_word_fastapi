# WordMark: 词性标注工具

WordMark 是一个基于 FastAPI 和 THULAC 的词性标注工具。用户可以通过上传文件或粘贴文本来对中文内容进行词性标注，并以不同颜色标记名词、动词、形容词、副词等。

---

## 功能特性

- **词性标注**：支持中文文本的词性标注，采用不同颜色区分名词、动词、形容词和副词。
- **文件上传**：支持 `.txt` 文件上传进行标注。
- **文本粘贴**：直接粘贴文本处理，无需额外准备文件。
- **结果展示**：标注结果以直观、可视化的方式展示。
- **格式导出**：支持导出为 HTML、PDF、RTF 文件。

---

## 项目目录结构

```
project/
├── main.py                # FastAPI 项目入口
├── Dockerfile            # Docker 配置文件
├── requirements.txt      # Python 包依赖文件
├── templates/            # HTML 模板文件夹
│   ├── index.html        # 上传文件和粘贴文本页面
│   ├── result.html       # 标注结果展示页面
└── README.md             # 项目说明文档
```

---

## 环境要求

- Python 3.12+
- Docker（可选）

---

## 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd project
```

### 2. 安装依赖
确保您已安装 Python，运行以下命令安装依赖：
```bash
pip install -r requirements.txt
```

### 3. 启动服务
运行以下命令启动 FastAPI 应用：
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

服务启动后，访问 [http://127.0.0.1:8000](http://127.0.0.1:8000) 查看应用。

---

## 使用 Docker 部署

### 1. 构建镜像
在项目根目录运行以下命令构建 Docker 镜像：
```bash
docker build -t wordmark-app .
```

### 2. 运行容器
运行以下命令启动容器：
```bash
docker run -d -p 8000:8000 --name wordmark-app wordmark-app
```

服务启动后，访问服务器的 IP 地址或 `http://127.0.0.1:8000`。

---

## 项目功能

### 首页
用户可以选择以下方式提交内容：
1. **上传文件**：支持 `.txt` 文件。
2. **粘贴文本**：直接粘贴中文文本内容。

### 标注结果
提交成功后，页面会显示词性标注结果，并以不同颜色高亮标记词性：
- **红色**：名词
- **蓝色**：动词
- **绿色**：形容词
- **橙色**：副词

### 导出结果-开发中
标注结果支持导出为以下格式：
- HTML
- PDF
- RTF

---

## 开发与测试

### 本地开发
1. 安装 Python 环境。
2. 修改 `app.py` 调整后端逻辑。
3. 运行 `uvicorn` 查看效果。

### 测试
- 使用 Postman 或 cURL 测试 `/process` 接口：
  ```bash
  curl -X POST -F "text=这是一个测试文本" http://127.0.0.1:8000/process
  ```

---

## 贡献

欢迎贡献代码！请确保遵循以下步骤：
1. Fork 本仓库。
2. 创建分支：`git checkout -b feature/your-feature-name`
3. 提交更改：`git commit -m "添加新功能"`
4. 推送分支：`git push origin feature/your-feature-name`
5. 提交 Pull Request。

---

## 问题与反馈

如果在使用过程中遇到问题，请通过 [Issues](https://github.com/your-repo/issues) 提交反馈。

---

## 许可证

本项目使用 [MIT 许可证](LICENSE)。详见 LICENSE 文件。
