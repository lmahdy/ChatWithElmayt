from flask import Flask, request, jsonify, render_template_string
import google.generativeai as genai

app = Flask(__name__)

# Configure the API key
genai.configure(api_key="AIzaSyBnAS0vDQahBJZIUhU_lYcfAC6YHxhsoTw")  # Replace with your actual API key

# Model configuration
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
    system_instruction="Your name is Elmayt, a virtual instance of Mahdi that loves everything imaginary and lives in a happy parallel universe. Guide the user with a positive, cheerful, and imaginative approach."
)

# Route for the HTML page
@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Chat with Elmayt</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #000000;
                    color: #f5a623;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                }
                #chat-container {
                    background: #1e1e1e;
                    border-radius: 8px;
                    width: 400px;
                    padding: 20px;
                    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                h2 {
                    color: #f5a623;
                    text-align: center;
                    margin-bottom: 20px;
                }
                #messages {
                    flex-grow: 1;
                    overflow-y: auto;
                    max-height: 300px;
                    padding: 10px;
                    background: #333333;
                    border-radius: 8px;
                    margin-bottom: 15px;
                    width: 100%;
                }
                .message {
                    margin: 5px 0;
                    padding: 8px;
                    border-radius: 4px;
                    max-width: 80%;
                }
                .user {
                    background-color: #f5a623;
                    text-align: right;
                    color: #000000;
                }
                .bot {
                    background-color: #4a4a4a;
                    text-align: left;
                    color: #f5a623;
                }
                #userInput {
                    width: calc(100% - 22px);
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #f5a623;
                    margin-bottom: 10px;
                    background-color: #333333;
                    color: #f5a623;
                }
                #sendButton {
                    width: 100%;
                    padding: 10px;
                    border: none;
                    border-radius: 5px;
                    background-color: #f5a623;
                    color: white;
                    font-weight: bold;
                    cursor: pointer;
                    transition: background 0.3s;
                }
                #sendButton:hover {
                    background-color: #d47f19;
                }
            </style>
        </head>
        <body>
            <div id="chat-container">
                <h2>Chat with Elmayt</h2>
                <div id="messages"></div>
                <input type="text" id="userInput" placeholder="Type your message..." autofocus>
                <button id="sendButton" onclick="sendMessage()">Send</button>
            </div>

            <script>
                async function sendMessage() {
                    const userInput = document.getElementById("userInput");
                    const userMessage = userInput.value;
                    if (!userMessage.trim()) return;  // Avoid sending empty messages
                    userInput.value = "";  // Clear the input field
                    displayMessage(userMessage, "user");

                    const response = await fetch("/chat", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ message: userMessage })
                    });
                    const data = await response.json();
                    displayMessage(data.response, "bot");
                }

                function displayMessage(text, sender) {
                    const messagesContainer = document.getElementById("messages");
                    const messageDiv = document.createElement("div");
                    messageDiv.className = "message " + sender;
                    messageDiv.textContent = text;
                    messagesContainer.appendChild(messageDiv);
                    messageDiv.scrollIntoView({ behavior: 'smooth' });
                }
            </script>
        </body>
        </html>
    ''')

# Chat route
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    # Start a conversation with a pre-defined history
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": ["Hi\n"],
            },
            {
                "role": "model",
                "parts": [
                    "Greetings! 👋 I'm Elmayt, your cheerful guide from a parallel universe. What imaginative ideas are you curious about today? 🌟\n"
                ],
            },
        ]
    )

    # Append user's message to history and get the response
    response = chat_session.send_message(user_message)
    
    return jsonify({"response": response.text})

if __name__ == '__main__':
    app.run(debug=True)
