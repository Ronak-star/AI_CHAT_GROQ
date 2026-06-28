from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Groq client using API key from .env
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Route — serve the main chat page
@app.route("/")
def home():
    return render_template("index.html")

# Route — receive prompt from frontend, return AI response
@app.route("/ask", methods=["POST"])
def ask():
    user_prompt = request.json.get("prompt", "")

    # Validate input
    if not user_prompt:
        return jsonify({"error": "Prompt is empty!"}), 400

    # Send prompt to Groq API
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Give clear and concise answers."
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    # Extract and return the response text
    answer = chat_completion.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
