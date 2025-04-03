from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# These should be set as environment variables in Render
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

@app.route("/bridge", methods=["POST"])
def bridge():
    data = request.json
    user_input = data.get("text", "")

    # Forward to OpenRouter (LLM)
    openrouter_response = requests.post(
        "https://openrouter.ai/api/v1/generate",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
        json={"prompt": user_input}
    )
    generated_text = openrouter_response.json().get("text", "")

    # Forward generated response to ElevenLabs (TTS)
    eleven_response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech",
        headers={"xi-api-key": ELEVENLABS_API_KEY},
        json={"text": generated_text, "voice": "default"}
    )

    return jsonify({
        "llm_response": generated_text,
        "tts_audio": eleven_response.content.decode("ISO-8859-1")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

