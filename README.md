# aiurl

Fetches a URL and passes the content to the OpenAI API to generate a summary. Can also accept different prompt files to experiment with different prompts. This script is useful for testing different prompts and seeing how they affect the output.

## Setup

You need to set the following environment variables (or specify them in a .env file):

```bash
OPENAI_API_KEY=your_openai_api_key
```

Before running, you will also need to install the required Python packages. I highly suggest using a venv to avoid conflicts with other Python packages.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

As a convenience mechanism, I have included a zsh shell script (that should be bash compatible although I haven't tested it) called `aiurl` that will act as a friendly cli tool rather than having to run the python script directly. To use it, you will need to edit to it make sure the paths are correct, copy it to directory in your path, and make it executable:

## Usage

```bash
python aiurl.py [-h] [-f FILE] [-r] url

Fetch URL content and process it with OpenAI.

positional arguments:
  url                   URL to fetch content from

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  JSON file to use as a prompt template
  -r, --retain-html     Retain HTML content without stripping tags
```
