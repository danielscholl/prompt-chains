# LLM Hello World App

A simple Python application demonstrating the use of various LLM libraries including Anthropic's Claude.

## Setup Instructions

1. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

2. Install required packages:
```bash
uv pip install llm openai python-dotenv llm-claude-3 anthropic
```

3. Create a `.env` file in the root directory with your API keys:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

4. Run the application:
```bash
python main.py
```

## Required Dependencies
- llm
- openai
- python-dotenv
- llm-claude-3
- anthropic

## Features
- Demonstrates basic setup of Anthropic's Claude client
- Shows integration with multiple LLM libraries
- Simple Hello World interaction with Claude-3

## Note
Make sure to replace the API keys in `.env` with your actual keys. Never commit API keys to version control.
