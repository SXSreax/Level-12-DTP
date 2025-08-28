import os
from flask import request, jsonify, Blueprint
from openai import OpenAI, APIError
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

chat_bp = Blueprint('chat', __name__)

endpoint = "https://models.github.ai/inference"
client = OpenAI(
    base_url=endpoint,
    api_key=os.getenv("OPENAI_API_KEY")
)


@chat_bp.route('/chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    if not data or 'userMsg' not in data:
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
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            model="gpt-4o",
            temperature=0.7,
            max_tokens=1024,
        )
        ai_response = response.choices[0].message.content
        return jsonify({'message': ai_response})
    except APIError as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({
            'message': """Sorry, I am having trouble
            connecting to the AI service."""
        }), 503
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({
            'message': 'An unexpected error occurred.'
        }), 500
