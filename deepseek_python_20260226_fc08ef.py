from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configure OpenAI API
openai.api_key = os.getenv('OPENAI_API_KEY', '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')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        content_type = data.get('type')
        topic = data.get('topic')
        tone = data.get('tone', 'professional')
        length = data.get('length', 'medium')
        keywords = data.get('keywords', '')
        
        # Create prompt based on content type
        prompt = create_prompt(content_type, topic, tone, length, keywords)
        
        # Generate content using ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional content creator specializing in digital marketing and content strategy."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=get_max_tokens(length),
            temperature=0.7
        )
        
        generated_content = response.choices[0].message.content
        
        return jsonify({
            'success': True,
            'content': generated_content,
            'type': content_type
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_prompt(content_type, topic, tone, length, keywords):
    length_guide = {
        'short': '2-3 paragraphs',
        'medium': '4-5 paragraphs',
        'long': '6-8 paragraphs'
    }
    
    prompts = {
        'blog': f"""Write a {tone} blog post about '{topic}'. 
        Length: {length_guide[length]}. 
        Keywords to include: {keywords}.
        Requirements:
        - Start with an engaging headline
        - Include an introduction that hooks the reader
        - Use subheadings (H2, H3) to organize content
        - Add bullet points or numbered lists where appropriate
        - End with a compelling conclusion and call-to-action
        - Optimize for readability""",
        
        'youtube': f"""Create a YouTube video script about '{topic}'. 
        Tone: {tone}. 
        Length: {length_guide[length]}.
        Keywords: {keywords}
        Script structure:
        - Hook (first 15 seconds)
        - Introduction
        - Main content with key points
        - Engagement prompt (like, comment, subscribe)
        - Call to action
        - End screen suggestion""",
        
        'thumbnail': f"""Generate 5 attention-grabbing thumbnail text ideas for a video about '{topic}'.
        Tone: {tone}
        Requirements:
        - Each text should be under 40 characters
        - Create curiosity or urgency
        - Include power words
        - Make it clickable
        - Format as a numbered list""",
        
        'product': f"""Write a compelling product description for '{topic}'.
        Tone: {tone}
        Length: {length_guide[length]}
        Keywords: {keywords}
        Include:
        - Attention-grabbing headline
        - Problem statement
        - Product features and benefits
        - Social proof elements
        - Price justification
        - Strong call-to-action""",
        
        'seo': f"""Write an SEO-optimized article about '{topic}'.
        Tone: {tone}
        Length: {length_guide[length]}
        Target keywords: {keywords}
        Requirements:
        - Meta title (under 60 chars)
        - Meta description (under 160 chars)
        - URL slug suggestion
        - H1, H2, H3 headings with keywords
        - Internal linking suggestions
        - FAQ section
        - Keyword density appropriate""",
        
        'social': f"""Create 5 social media captions for Facebook/Instagram about '{topic}'.
        Tone: {tone}
        Keywords: {keywords}
        Each caption should include:
        - Engaging hook
        - Main message
        - Relevant emojis
        - Call-to-action
        - 10-15 relevant hashtags
        Format each caption separately with a line break between them."""
    }
    
    return prompts.get(content_type, prompts['blog'])

def get_max_tokens(length):
    tokens = {
        'short': 500,
        'medium': 1000,
        'long': 2000
    }
    return tokens.get(length, 1000)

if __name__ == '__main__':
    app.run(debug=True, port=5000)