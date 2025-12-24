def handle_message(message, client):
    """Acts as a research assistant for insights or explanations."""
    prompt = f"You are a research assistant. Answer this question or find key points:\n\n{message}"
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
