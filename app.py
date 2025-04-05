from flask import Flask, request, jsonify
import requests
import os
import uuid
import time
import hmac
import hashlib
import json

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEBHOOK_SECRET = b'wsec_63483bd02a32b231047aa065d19fe2df8f68958c8815fb5945106de992c2843b'

def verify_signature(signature, data):
    expected_signature = hmac.new(WEBHOOK_SECRET, msg=json.dumps(data).encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(signature, expected_signature)

@app.route("/v1/chat/completions", methods=["POST"])
def chat():
    data = request.json
    signature = request.headers.get('ElevenLabs-Signature')
    if not verify_signature(signature, data):
        return jsonify({'error': 'Invalid signature'}), 403

    messages = data.get("messages", [])
    model = "sophosympatheia/midnight-rose-70b"

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        json={
            "model": model,
            "messages": messages
        }
    )

    result = response.json()
    reply = result.get("choices", [{}])[0].get("message", {}).get("content", "")

    return jsonify({
        "id": f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": reply
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
