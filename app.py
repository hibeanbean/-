from flask import Flask, render_template, request
import os
from docx import Document
import fitz  # PyMuPDF

app = Flask(__name__)

# 提取 PDF 文本
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# 提取 .docx 文档文本
def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([p.text for p in doc.paragraphs])

# 假设发送到某个平台进行匹配度分析（用通义千问 API 或其他平台接口）
def get_match_score(jd_text, resume_text):
    # 这里假设调用一个平台API的函数（示例，具体要根据实际API来修改）
    # 可以参考文心一言或者通义千问API
    response = {
        "score": 85,  # 假设的评分
        "matches": ["技能匹配", "项目经验相关"],
        "gaps": ["缺乏团队管理经验", "语言能力不强"],
        "recommendation": "建议进入下一轮面试"
    }
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        job_desc = request.form["job_desc"]
        resume_file = request.files["resume_file"]
        
        # 处理简历文件
        if resume_file.filename.endswith(".pdf"):
            resume_text = extract_text_from_pdf(resume_file)
        elif resume_file.filename.endswith(".docx"):
            resume_text = extract_text_from_docx(resume_file)
        else:
            return "仅支持 .pdf 和 .docx 格式的简历"
        
        # 调用平台进行分析
        analysis_result = get_match_score(job_desc, resume_text)
        
        return render_template("result.html", result=analysis_result)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
