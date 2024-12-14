# Prompt Chain Examples

This repository demonstrates different prompt chain patterns using various LLM models (Google Gemini and Anthropic Claude).

## Setup

1. Install dependencies:
```bash
uv pip install llm
```

2. Create and activate a virtual environment using uv:
```bash
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
```

3. Install required packages:
```bash
uv pip install llm openai python-dotenv llm-claude-3 anthropic google-generativeai
```

4. Create a `.env` file in the root directory with your API keys:
```
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
```

5. Run the application:
```bash
uv run main.py
```

## Usage

Run the application with your chosen model and prompt chain:

```bash
uv run main.py --model [gemini|haiku|sonnet|opus] --chain [snowball|workers|fallback|decision|plan|human|self-correct]
```

Examples:
```bash
# Run default (Gemini model with snowball chain)
uv run main.py

# Use Gemini model with workers chain
uv run main.py --chain workers

# Use Claude 3 Haiku with fallback chain
uv run main.py --model haiku --chain fallback

# Use Claude 3 Sonnet with decision maker chain
uv run main.py --model sonnet --chain decision
```

### Available Prompt Chains

- `snowball`: Builds information progressively (default)
- `workers`: Delegates tasks to individual prompts
- `fallback`: Uses multiple models with fallback logic
- `decision`: Uses prompts to control flow
- `plan`: Separates planning and execution
- `human`: Incorporates human feedback
- `self-correct`: Reviews and corrects its own output

## Required Dependencies
- llm
- openai
- python-dotenv
- llm-claude-3
- anthropic
- google-generativeai

## Features
- Demonstrates basic setup of Anthropic's Claude client
- Shows integration with multiple LLM libraries
- Simple Hello World interaction with Claude-3

## Note
Make sure to replace the API keys in `.env` with your actual keys. Never commit API keys to version control.
