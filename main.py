import os
from dotenv import load_dotenv
import llm
import openai
from anthropic import Anthropic

# Load environment variables
load_dotenv()

def main():
    print("Hello World!")
    
    # Initialize Anthropic client
    anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    # Create a simple message
    message = anthropic.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": "Say hello world!"
        }]
    )
    
    print("\nClaude's response:")
    print(message.content[0].text)
    
    print("\nInstalled libraries:")
    print("- llm version:", llm.__version__)
    print("- openai version:", openai.__version__)
    print("- python-dotenv version:", os.getenv('PYTHON_DOTENV_VERSION', 'installed'))
    print("- llm-claude-3 is installed")
    print("- anthropic is installed")

if __name__ == "__main__":
    main()
