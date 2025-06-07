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

os.makedirs('posts', exist_ok=True)

HOME_PAGE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Blog Post Generator</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap">
    <style>
        :root {
            --primary-color: #20A4F3;
            --secondary-color: #59F8E8;
            --accent-color: #941C2F;
            --dark-color: #03191E;
            --light-color: #C1CFDA;
            --success-color: #59F8E8;
            --border-radius: 16px;
            --box-shadow: 0 10px 30px rgba(3, 25, 30, 0.15);
            --transition: all 0.3s ease;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Poppins', sans-serif;
            background: var(--light-color);
            color: var(--dark-color);
            min-height: 100vh;
            padding: 40px 20px;
            line-height: 1.6;
        }
        
        .wrapper {
            max-width: 1100px;
            margin: 0 auto;
        }
        
        header {
            text-align: center;
            margin-bottom: 50px;
            animation: fadeIn 1s ease-in-out;
            background-color: var(--dark-color);
            padding: 40px 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }
        
        h1 {
            font-size: 3rem;
            font-weight: 700;
            color: var(--secondary-color);
            margin-bottom: 15px;
            letter-spacing: -0.5px;
            position: relative;
            display: inline-block;
        }
        
        h1::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 4px;
            background: var(--accent-color);
            border-radius: 2px;
        }
        
        .tagline {
            font-size: 1.3rem;
            color: var(--light-color);
            max-width: 700px;
            margin: 20px auto 0;
        }
        
        .container {
            background-color: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 40px;
            margin-bottom: 40px;
            transition: var(--transition);
            animation: slideUp 0.8s ease-out;
            border-left: 6px solid var(--primary-color);
        }
        
        .container:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(3, 25, 30, 0.2);
        }
        
        h2 {
            font-size: 2rem;
            color: var(--primary-color);
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 3px solid var(--light-color);
        }
        
        .endpoint {
            background-color: var(--dark-color);
            color: var(--secondary-color);
            padding: 20px 25px;
            border-radius: var(--border-radius);
            font-family: 'Courier New', monospace;
            margin: 20px 0;
            border-left: 6px solid var(--accent-color);
            font-size: 1.2rem;
            overflow-x: auto;
        }
        
        .example {
            color: var(--dark-color);
            font-style: italic;
            margin: 20px 0;
            font-size: 1.1rem;
            background-color: rgba(193, 207, 218, 0.3);
            padding: 15px;
            border-radius: var(--border-radius);
        }
        
        .example a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 600;
            transition: var(--transition);
        }
        
        .example a:hover {
            color: var(--accent-color);
            text-decoration: underline;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 30px;
            margin-top: 35px;
        }
        
        .feature-card {
            background: white;
            padding: 30px;
            border-radius: var(--border-radius);
            text-align: center;
            transition: var(--transition);
            box-shadow: 0 5px 15px rgba(3, 25, 30, 0.1);
            border-bottom: 4px solid transparent;
        }
        
        .feature-card:nth-child(1) {
            border-bottom-color: var(--primary-color);
        }
        
        .feature-card:nth-child(2) {
            border-bottom-color: var(--secondary-color);
        }
        
        .feature-card:nth-child(3) {
            border-bottom-color: var(--accent-color);
        }
        
        .feature-card:nth-child(4) {
            border-bottom-color: var(--dark-color);
        }
        
        .feature-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 15px 30px rgba(3, 25, 30, 0.15);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            display: inline-block;
            background-color: rgba(193, 207, 218, 0.3);
            width: 80px;
            height: 80px;
            line-height: 80px;
            border-radius: 50%;
        }
        
        .feature-card:nth-child(1) .feature-icon {
            color: var(--primary-color);
        }
        
        .feature-card:nth-child(2) .feature-icon {
            color: var(--secondary-color);
        }
        
        .feature-card:nth-child(3) .feature-icon {
            color: var(--accent-color);
        }
        
        .feature-card:nth-child(4) .feature-icon {
            color: var(--dark-color);
        }
        
        .feature-title {
            font-weight: 700;
            margin-bottom: 15px;
            color: var(--dark-color);
            font-size: 1.3rem;
        }
        
        .feature-desc {
            font-size: 1rem;
            color: #555;
            line-height: 1.6;
        }
        
        footer {
            text-align: center;
            margin-top: 60px;
            color: var(--dark-color);
            font-size: 1rem;
            background-color: white;
            padding: 20px;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { 
                opacity: 0;
                transform: translateY(40px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @media (max-width: 768px) {
            h1 {
                font-size: 2.4rem;
            }
            
            .container {
                padding: 30px;
            }
            
            .features-grid {
                grid-template-columns: 1fr;
                gap: 20px;
            }
            
            .feature-card {
                padding: 25px;
            }
        }
    </style>
</head>
<body>
    <div class="wrapper">
        <header>
            <h1>AI Blog Post Generator</h1>
            <p class="tagline">Create SEO-optimized content with the power of artificial intelligence</p>
        </header>
        
        <div class="container">
            <h2>API Endpoints</h2>
            <p>Generate a blog post by making a GET request to:</p>
            <div class="endpoint">/generate?keyword=your_keyword</div>
            <p class="example">Example: <a href="/generate?keyword=smart%20home%20hub">/generate?keyword=smart%20home%20hub</a></p>
        </div>
        
        <div class="container">
            <h2>Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <div class="feature-title">SEO Optimized</div>
                    <div class="feature-desc">Content designed to rank well in search engines with data-driven keyword research</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔄</div>
                    <div class="feature-title">Daily Generation</div>
                    <div class="feature-desc">Automatic content creation on schedule to keep your blog fresh and updated</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🔗</div>
                    <div class="feature-title">Affiliate Links</div>
                    <div class="feature-desc">Seamless integration of monetization opportunities with strategic placement</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📝</div>
                    <div class="feature-title">HTML Format</div>
                    <div class="feature-desc">Ready-to-publish formatted content with proper semantic structure</div>
                </div>
            </div>
        </div>
        
        <footer>
            &copy; 2023 AI Blog Post Generator | Powered by OpenAI GPT-4
        </footer>
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
    keyword = "smart home hub"
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
        seo_data = seo_fetcher.get_seo_data(keyword)
        content = ai_generator.generate_blog_post(keyword, seo_data)
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
    scheduler.add_job(generate_daily_post, 'cron', hour=0)
    scheduler.start()
    
    app.run(debug=True) 