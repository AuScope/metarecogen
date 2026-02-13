
import ollama

# Choose your model
# Run 'ollama pull deepseek-r1:8b' to fetch it
model = "deepseek-r1:8b"

def ollama_summary(text: str) -> str:

    # Create a summarization prompt
    prompt = f"Summarize the following text:\n{text}"

    # Generate the summary
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

    # Return the result
    return response['message']['content']
