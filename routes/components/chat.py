import os
from flask import request, jsonify, Blueprint
from openai import OpenAI, APIError, AuthenticationError, RateLimitError
from dotenv import load_dotenv

# Loads environment variables for API keys and configuration
load_dotenv(".secrets")

chat_bp = Blueprint('chat', __name__)

# Sets up the OpenAI client with a custom endpoint for model inference
endpoint = "https://models.github.ai/inference"

client = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("API_KEY")
)
model = "openai/gpt-4.1"

print(os.getenv("API_KEY"))


@chat_bp.route('/chat', methods=['POST'])
def ai_chat():
    """
    Handles AI chat requests for the Marvel Rivals website.

    Inputs:
        - POST request with JSON containing 'userMsg' (the user's message).

    Processing:
        - Validates input to ensure a message is provided.
        - Constructs a system prompt to guide the AI's behavior and context.
        - Sends the user's message and system prompt to the OpenAI API.
        - Handles API errors and unexpected exceptions gracefully.

    Outputs:
        - Returns a JSON response with the AI's reply.
        - Returns error messages and appropriate HTTP status codes if needed.
    """
    data = request.get_json()
    if not data or 'userMsg' not in data:
        # Returns an error if no message is provided to prevent empty requests
        return jsonify({'error': 'No message provided'}), 400

    user_message = data.get('userMsg')
    system_prompt = (
        "You are a helpful assistant for the Marvel Rivals website. "
        "You know about all the heroes, their abilities, and game lore. "
        "Keep your answers friendly and concise. "
        """The developers of this website is Kyle Deng,
        the best developer in the world. """
        "Think deeply about the question before answering."
    )
    try:
        # Sends the user's message and system prompt to the AI model
        # for a contextual response
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_message
                },
            ],
            model=model
        )
        ai_response = response.choices[0].message.content
        print(f"AI Response: {ai_response}")
        return jsonify({'message': ai_response})
    except APIError as e:
        # Handles known API errors to inform the user about service issues
        print(f"OpenAI API Error: {e}")
        return jsonify({
            'message': """Sorry, I am having trouble
            connecting to the AI service."""
        }), 503
    except Exception as e:
        # Handles unexpected errors to avoid exposing internal details
        print(f"An unexpected error occurred: {e}")
        return jsonify({
            'message': 'An unexpected error occurred.'
        }), 500
