

# AI Instagram Caption Generator

Generate creative Instagram captions instantly using AI.

## Description
This web app takes an image or a short description as input and generates 3–4 Instagram captions categorized by style (e.g., Funny, Inspirational, Romantic). Built with Flask and AI API integration, it’s perfect for content creators and social media enthusiasts.

## Features
- Generate multiple captions from a photo or text description
- Categorizes captions by style
- Fast and easy to use
- Built with Flask and AI API

## Installation

1. Clone the repository:
```bash
git clone https://github.com/MohammedAthiq/ai-instagram-caption-generator.git
cd ai-instagram-caption-generator
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export GOOGLE_API_KEY=<your-Gemini-API-key>   # Mac/Linux
set GOOGLE_API_KEY=<your-Gemini-API-key>      # Windows
```

5. Run the app locally:
```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Project Structure
```
ai-instagram-caption-generator/
│
├── app.py             # Main Flask app
├── requirements.txt   # Python dependencies
├── templates/         # HTML templates
├── static/            # CSS/JS files
└── README.md
```

## License
MIT License