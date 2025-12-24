def handle_message(message, client):
    """Provides coding assistance or code explanations."""
    prompt = f"You are a helpful coding assistant. Respond to this request:\n\n{message}"
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
