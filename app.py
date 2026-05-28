from flask import Flask,render_template,request,jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = "sk-0ae69d3b8ced4a28897f77e4503fbaac"
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save",methods=["POST"])
def save():
    data = request.json
    text = data.get("text","")
    filename = data.get("filename","my_text.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

    return jsonify({"message":"保存成功","filename":filename})

@app.route("/open",methods=["POST"])
def open_file():
    data = request.json
    filename = data.get("filename","my_text.txt")

    try:
        with open(filename, "r", encoding="utf-8") as f:
            text = f.read()
        return jsonify({"text":text})
    except FileNotFoundError:
        return jsonify({"error":"找不到这个文件"}),404

@app.route("/explain", methods=["POST"])
def explain():
    data = request.json
    selected_text = data.get("text","")
    custom_prompt = data.get("prompt",
    "你是语言学习助手。"
    "直接给出选中内容在本文中的意思，"
    "不要任何开场白，不要markdown符号，不要星号井号引号，"
    "不要解释其他语境，只解释它在这篇文章里的用法。"
    "单词需要美式音标。"
    "禁止使用这样的形式**“环境”**,用双引号""即可"
    "错误的回答方式为'- **在网页/UI设计(用户界面)中**:'，而正确的方式为'・在网页/UI设计(用户界面)中'"
    "用中文回答的时候，符号系统仍使用英文键盘"
    "回答限制在50-100个字以内，包括标点符号"
    )
    article_context = data.get("content","")
    


    messages = [
        {"role":"user","content":f"{custom_prompt}\n\n文章原文: {article_context}\n\n用户选中的内容: {selected_text}"}
    ]

    headers = {
        "Authorization": f"Bearer sk-0ae69d3b8ced4a28897f77e4503fbaac",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 300
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=headers,json=payload)
        result = response.json()
        explanation = result["choices"][0]["message"]["content"]
        return jsonify({"explanation":explanation})
    except Exception as e:
        return jsonify({"error":str(e)}),500
    
if __name__ == "__main__":
    app.run(debug=True,port=5000)
