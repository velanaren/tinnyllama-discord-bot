# server.py
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

# Update this with your model path
MODEL_PATH = "../models/tinyllama/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
LLAMA_BIN = "./llama.cpp/build/bin/llama-simple"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")
    tokens = data.get("max_tokens", 100)

    try:
        result = subprocess.run(
            [LLAMA_BIN, "-m", MODEL_PATH, "-p", prompt, "-n", str(tokens)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return jsonify({
            "output": result.stdout.strip()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
