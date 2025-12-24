def handle_message(message, client):
    """Summarizes user text input."""
    prompt = f"Summarize the following text in a clear, concise paragraph:\n\n{message}"
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content
