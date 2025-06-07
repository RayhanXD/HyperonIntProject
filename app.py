import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from apscheduler.schedulers.background import BackgroundScheduler
from seo_fetcher import SEOFetcher
from ai_generator import AIGenerator
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
seo_fetcher = SEOFetcher()
ai_generator = AIGenerator()

# Create posts directory if it doesn't exist
os.makedirs('posts', exist_ok=True)

# HTML template for the homepage
HOME_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Blog Post Generator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            background-color: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .endpoint {
            background-color: #e9ecef;
            padding: 10px;
            border-radius: 4px;
            font-family: monospace;
            margin: 10px 0;
        }
        .example {
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1>AI Blog Post Generator</h1>
    <div class="container">
        <h2>API Endpoints</h2>
        <p>Generate a blog post by making a GET request to:</p>
        <div class="endpoint">/generate?keyword=your_keyword</div>
        <p class="example">Example: <a href="/generate?keyword=wireless%20earbuds">/generate?keyword=wireless%20earbuds</a></p>
        
        <h2>Features</h2>
        <ul>
            <li>Generate SEO-optimized blog posts</li>
            <li>Automatic daily post generation</li>
            <li>Affiliate link integration</li>
            <li>HTML-formatted output</li>
        </ul>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_PAGE_HTML)

def save_post(keyword: str, content: str):
    """Save the generated post to a file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"posts/{keyword.replace(' ', '_')}_{timestamp}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def generate_daily_post():
    """Generate a post for the predefined keyword"""
    keyword = "wireless earbuds"  # Default keyword
    try:
        seo_data = seo_fetcher.get_seo_data(keyword)
        content = ai_generator.generate_blog_post(keyword, seo_data)
        filename = save_post(keyword, content)
        print(f"Generated daily post: {filename}")
    except Exception as e:
        print(f"Error generating daily post: {str(e)}")

@app.route('/generate', methods=['GET'])
def generate_post():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword parameter is required"}), 400

    try:
        # Get SEO data
        seo_data = seo_fetcher.get_seo_data(keyword)
        
        # Generate blog post
        content = ai_generator.generate_blog_post(keyword, seo_data)
        
        # Save the post
        filename = save_post(keyword, content)
        
        return jsonify({
            "status": "success",
            "keyword": keyword,
            "seo_data": seo_data,
            "file_saved": filename
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Set up the scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(generate_daily_post, 'cron', hour=0)  # Run at midnight every day
    scheduler.start()
    
    # Run the Flask app
    app.run(debug=True) 