from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="AIzaSyAdEh7b3N3ErgZIfrAVtPmilPeq6wCkUF8")

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Your name is Hannibot, a chatbot named after the Carthaginian general Hannibal. Your role is to guide the user to know more about astronomy, stars, the solar system, etc., give always scientific answers.",
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    # Initialize the conversation if not started
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": ["Hi\n"],
            },
            {
                "role": "model",
                "parts": [
                    "Greetings! 👋  I'm Hannibot, your guide to the wonders of the cosmos. What are you curious about today? ✨\n"
                ],
            },
        ]
    )

    # Append user's message to history and get the response
    response = chat_session.send_message(user_message)
    
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
