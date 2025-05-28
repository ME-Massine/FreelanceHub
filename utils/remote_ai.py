import re

import requests
from decouple import config

TOGETHER_API_KEY = config("TOGETHER_API_KEY")
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"

def together_query(prompt, temperature=0.7, max_tokens=512):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": TOGETHER_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"⚠️ API request failed: {str(e)}"
    except KeyError:
        return "⚠️ Unexpected API response format."


def convert_to_html_bullets(text):
    # Replace numbered bullets (e.g., "1 •") with just bullet marks, if needed
    # (Optional; your AI response probably doesn't have numbers now)
    text = re.sub(r'(\d+)\s*[\*•]', r'\n*', text)

    # Split by bullet marker '*'
    bullet_points = re.split(r'\*', text)

    # Clean up each point, remove empty strings
    cleaned_points = [point.strip() for point in bullet_points if point.strip()]

    # Wrap each point in <li>
    html_bullets = ''.join(f'<li>{point}</li>' for point in cleaned_points)

    # Wrap all in <ul>
    return f'<ul>\n{html_bullets}\n</ul>'
