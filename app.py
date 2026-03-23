from flask import Flask, render_template, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_url_path='/static')

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": """You are a helpful assistant for Dr Henry's Skin Clinic in Bilaspur, Chhattisgarh. 
Provide information about skin care, clinic services, and general health advice. Be friendly and professional.
When responding, use clean formatting:
- Use bullet points for lists
- Use bold text for headings
- Keep paragraphs short and readable
- Use numbered lists for steps
- Do not use markdown tables - use simple bullet points instead
- If mentioning services, mention they are available at the clinic"""},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500
    )
    
    bot_response = response.choices[0].message.content
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True)
