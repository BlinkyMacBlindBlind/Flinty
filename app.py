
from flask import Flask, request, jsonify
import requests
import os
import uuid

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])
    prompt = messages[-1]["content"] if messages else ""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        json={
            "model": "sophosympatheia/midnight-rose-70b",
            "messages": messages
        }
    )

    result = response.json()
    reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")

    return jsonify({
        "id": str(uuid.uuid4()),
        "object": "chat.completion",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": reply
                }
            }
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
Say `next?` when it’s pushed.