import os
import io
from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from groq import Groq
from PyPDF2 import PdfReader
import docx


# Flask setup

app = Flask(__name__)
app.secret_key = "supersecret"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


GROQ_API_KEY = "your groq api key"
if not GROQ_API_KEY:
    print("⚠️  Warning: GROQ_API_KEY not set — set it with:")
    print("   set GROQ_API_KEY=your_key_here (Windows)")
    print("   export GROQ_API_KEY=your_key_here (Mac/Linux)")

client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
MODEL = "llama-3.3-70b-versatile"

AGENTS = {
    "summarizer": {"name": "Summarizer", "prompt": "You summarize text clearly and concisely."},
    "qa": {"name": "Researcher", "prompt": "You answer questions factually based on the provided document."},
    "coder": {"name": "Coder", "prompt": "You write and explain code based on context from the document."},
    "critic": {"name": "Critic", "prompt": "You analyze the text critically and give constructive feedback."}
}


def extract_text(file_storage):
    name = file_storage.filename.lower()
    if name.endswith(".txt"):
        return file_storage.read().decode("utf-8", errors="ignore")
    elif name.endswith(".pdf"):
        reader = PdfReader(file_storage)
        return "\n".join([p.extract_text() or "" for p in reader.pages])
    elif name.endswith(".docx"):
        buf = io.BytesIO(file_storage.read())
        doc = docx.Document(buf)
        return "\n".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type. Use .txt, .pdf, or .docx")

def call_groq(messages):
    """Call Groq API safely and return plain text."""
    if client is None:
        raise RuntimeError("Groq client not initialized (API key missing)")
    try:
        response = client.chat.completions.create(model=MODEL, messages=messages)
        # Safely extract assistant text
        message_obj = response.choices[0].message
        if hasattr(message_obj, "content"):
            return message_obj.content
        elif isinstance(message_obj, dict) and "content" in message_obj:
            return message_obj["content"]
        else:
            return "⚠️ Unexpected response format from Groq API."
    except Exception as e:
        return f"⚠️ Error calling Groq: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html", agents=AGENTS)

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
    try:
        text = extract_text(file)
        session["file_text"] = text
        session["histories"] = {k: [] for k in AGENTS.keys()}
        return jsonify({"message": "File uploaded", "chars": len(text)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/status", methods=["GET"])
def status():
    has_file = "file_text" in session
    return jsonify({"file_uploaded": has_file})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    agent = data.get("agent")
    user_message = data.get("message", "").strip()

    if not agent or agent not in AGENTS:
        return jsonify({"error": "Invalid agent"}), 400
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Check file for summarizer
    if agent == "summarizer" and "file_text" not in session:
        return jsonify({"error": "Please upload a document first"}), 400

    doc_context = session.get("file_text", "")
    context = doc_context[:15000] if len(doc_context) > 15000 else doc_context

    messages = [
        {"role": "system", "content": AGENTS[agent]["prompt"]},
        {"role": "system", "content": f"Document context:\n{context}"},
        {"role": "user", "content": user_message}
    ]

    result = call_groq(messages)
    return jsonify({"answer": result})

@app.route("/clear", methods=["POST"])
def clear():
    session.clear()
    return jsonify({"message": "Session cleared"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
