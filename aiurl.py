import os
import sys
import argparse
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import json
import tiktoken

def load_env():
    load_dotenv()
    return os.getenv('OPENAI_API_KEY')

def fetch_url_content(url, retain_html):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch the URL content.")
        sys.exit(1)

    if retain_html:
        return response.text

    return BeautifulSoup(response.text, 'html.parser').get_text()

def split_content(content, token_limit=16_000, encoding_name="cl100k_base"):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(content)
    parts = []
    start = 0

    while start < len(tokens):
        end = start + token_limit
        if end > len(tokens):
            end = len(tokens)
        part = encoding.decode(tokens[start:end])
        parts.append(part)
        start = end

    return parts

def process_with_openai(content_parts, prompt_template, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    responses = []
    for part in content_parts:
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        prompt = json.loads(prompt_template)
        prompt['messages'][0]['content'] = part

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=prompt
        )

        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            responses.append(result)
        else:
            print(f"API error: {response.status_code} - {response.text}")
            sys.exit(1)

    return '\n\n'.join(responses)

def main(url, filepath, retain_html):
    api_key = load_env()
    if not api_key:
        print("OPENAI_API_KEY not found in environment variables.")
        sys.exit(1)

    with open(filepath, 'r') as file:
        template = file.read()

    content = fetch_url_content(url, retain_html)
    content_parts = split_content(content)
    combined_response = process_with_openai(content_parts, template, api_key)
    print(combined_response)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch URL content and process it with OpenAI.')
    parser.add_argument('url', help='URL to fetch content from')
    parser.add_argument('-f', '--file', default='default.json', help='JSON file to use as a prompt template')
    parser.add_argument('-r', '--retain-html', action='store_true', help='Retain HTML content without stripping tags')
    args = parser.parse_args()

    main(args.url, args.file, args.retain_html)
