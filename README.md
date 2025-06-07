# AI-Powered Blog Post Generator

This Flask application automatically generates SEO-optimized blog posts using OpenAI's GPT-4 model. It includes a daily scheduler to automatically generate posts for predefined keywords.

## Features

- Generate blog posts from any keyword
- SEO data analysis (mock data included)
- Automatic daily post generation
- Affiliate link integration
- HTML-formatted output
- File-based storage of generated posts

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-blog-generator
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Running the Application

Start the Flask application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

### API Endpoints

#### Generate a Blog Post
```
GET /generate?keyword=<your_keyword>
```

Example:
```bash
curl "http://localhost:5000/generate?keyword=wireless%20earbuds"
```

### Daily Post Generation

The application automatically generates a post for the keyword "wireless earbuds" at midnight every day. The generated posts are saved in the `posts` directory with timestamps in their filenames.

## Project Structure

- `app.py`: Main Flask application
- `seo_fetcher.py`: SEO data fetching module
- `ai_generator.py`: OpenAI integration for blog post generation
- `posts/`: Directory where generated posts are stored
- `requirements.txt`: Python dependencies
- `.env`: Environment variables (not tracked in git)

## Customization

### Changing the Default Keyword

To change the default keyword for daily posts, modify the `keyword` variable in the `generate_daily_post()` function in `app.py`.

### Modifying SEO Data

The mock SEO data can be modified in the `SEOFetcher` class in `seo_fetcher.py`.

### Adjusting Blog Post Generation

The blog post generation parameters can be modified in the `AIGenerator` class in `ai_generator.py`.

## Error Handling

The application includes basic error handling for:
- Missing API keys
- Invalid keywords
- OpenAI API errors
- File system errors

## Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- The application runs in debug mode by default (not recommended for production)

## License

MIT License 