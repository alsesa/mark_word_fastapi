# from docx import Document
import os
from tempfile import NamedTemporaryFile

import thulac
from fastapi import FastAPI, Form, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class ExportRequest(BaseModel):
    format: str  # 导出格式（html、pdf、rtf）
    content: str  # 要导出的内容

# 初始化 THULAC 分词工具
thu = thulac.thulac()

# 初始化 FastAPI 应用和模板
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, file: UploadFile = File(None), text: str = Form(None)):
    """
        统一处理上传文件和粘贴文本，返回标注结果页面
        """
    if file:
        # 读取上传文件内容
        content = await file.read()
        text_content = content.decode("utf-8")
    elif text:
        # 读取粘贴文本内容
        text_content = text
    else:
        return templates.TemplateResponse(
            "error.html", {"request": request, "message": "未提供文件或文本"}
        )

    # 处理文本，返回标注结果
    processed_text = process_text(text)

    return templates.TemplateResponse("result.html", {"request": request, "content": processed_text})


def process_text(text: str) -> str:
    """处理文本并为每种词性添加 CSS 类，同时保留段落换行"""
    words = thu.cut(text)
    colored_text = ""

    for word, tag in words:
        if tag:  # 确保 tag 不为空
            colored_text += f"<span class='word {tag[0]}'>{word}</span>"
        else:
            colored_text += word  # 没有词性时直接添加词语

    # 替换换行符为 <br>
    return colored_text.replace("\n", "<br>")



@app.post("/export")
async def export_file(request: ExportRequest):
    format = request.format
    content = request.content

    if format == "html":
        file_name = "exported_result.html"
        file_content = f"<html><body>{content}</body></html>"
        return create_file_response(file_name, file_content.encode("utf-8"), "text/html")

    elif format == "pdf":
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            generate_pdf(temp_file.name, content)
            return FileResponse(temp_file.name, filename="exported_result.pdf", media_type="application/pdf")

    elif format == "rtf":
        file_name = "exported_result.rtf"
        file_content = generate_rtf(content)
        return create_file_response(file_name, file_content.encode("utf-8"), "application/rtf")

    return {"error": "Unsupported format"}


def create_file_response(file_name, file_content, media_type):
    """
    创建文件响应
    """
    with NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_name)[1]) as temp_file:
        temp_file.write(file_content)
        temp_file.flush()
        return FileResponse(temp_file.name, filename=file_name, media_type=media_type)


def generate_pdf(file_path, content):
    """
    生成 PDF 文件
    """
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)
    width, height = letter
    y = height - 40

    for line in content.split("<br>"):
        c.drawString(40, y, line.strip())
        y -= 20
        if y < 40:  # 换页条件
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 40
    c.save()


def generate_rtf(content):
    """
    生成 RTF 文件
    """
    rtf_header = r"{\rtf1\ansi\deff0"
    rtf_footer = r"}"
    rtf_body = content.replace("<br>", r"\line ")
    return rtf_header + rtf_body + rtf_footer

