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
    custom_prompt = data.get("prompt","你是语言学习助手。根据上下文解释选中内容，给出中文意思，单词需要美式音标。回答要简洁，根据内容难度和长度灵活调整")

    messages = [
        {"role":"user","content":f"{custom_prompt}\n\n{selected_text}"}
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
