import os
from flask import request, jsonify, Blueprint
from openai import OpenAI, APIError
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

chat_bp = Blueprint('chat', __name__)

# CRITICAL SECURITY WARNING:
# The API key you had here was a GitHub Personal Access Token.
# 1. You have exposed it publicly. Please go to your GitHub settings
#    and REVOKE this token IMMEDIATELY.
# 2. To use the OpenAI API, you need a key from platform.openai.com.
# 3. NEVER hardcode API keys in your code. The code below now uses
#    environment variables, which is the secure way to handle secrets.
endpoint = "https://models.github.ai/inference"
client = OpenAI(
    base_url=endpoint,
    # The API key is now read securely from your .env file
    api_key=os.getenv("OPENAI_API_KEY")
    # The base_url you were using is for Azure. If you are using the standard
    # OpenAI API, you should REMOVE the base_url parameter. The library
    # will use the correct default.
    # base_url="https://models.inference.ai.azure.com",
)

@chat_bp.route('/chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    if not data or 'userMsg' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data.get('userMsg')
    try:
        system_prompt = (
            "You are a helpful assistant for the Marvel Rivals website. "
            "You know about all the heroes, their abilities, and game lore. "
            "Keep your answers friendly and concise."
        )
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model="gpt-4o",
            temperature=0.7, # Lowered for more focused answers
            max_tokens=1024, # Reduced to save on costs
        )
        ai_response = response.choices[0].message.content
        return jsonify({'message': ai_response})
    except APIError as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({'message': 'Sorry, I am having trouble connecting to the AI service.'}), 503
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({'message': 'An unexpected error occurred.'}), 500