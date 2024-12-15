import os
from dotenv import load_dotenv
import json
import llm
import google.generativeai as genai
import argparse
import random

load_dotenv()
os.environ['GRPC_PYTHON_LOG_LEVEL'] = '0'

# ------ Helpers Methods
def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Run different prompt chain patterns with various LLM models.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Run with default settings (Gemini model, snowball chain)
  uv run main.py

  # Use specific model and chain
  uv run main.py --model haiku --chain workers

  # Run snowball chain with Gemini
  uv run main.py --model gemini --chain snowball

Chain Descriptions:
  snowball     - Builds information progressively (good for content creation)
  workers      - Delegates tasks to individual prompts (good for parallel tasks)
  fallback     - Uses multiple models with fallback logic (good for reliability)
  decision     - Uses prompts to control flow (good for dynamic responses)
  plan         - Separates planning and execution (good for complex tasks)
  human        - Incorporates human feedback (good for iterative refinement)
  self-correct - Reviews and corrects its own output (good for accuracy)

Models Available:
  gemini       - Google's Gemini Flash model (fast, good for general use)
  haiku        - Claude 3 Haiku (fast, good for simple tasks)
  sonnet       - Claude 3 Sonnet (balanced performance)
  opus         - Claude 3 Opus (powerful, good for complex tasks)
''')

    parser.add_argument(
        '--model',
        type=str,
        choices=['gemini', 'haiku', 'sonnet', 'opus'],
        default='gemini',
        help='Model to use for prompts (default: %(default)s)'
    )

    parser.add_argument(
        '--chain',
        type=str,
        choices=['snowball', 'workers', 'fallback', 'decision', 'plan', 'human', 'self-correct'],
        default='snowball',
        help='Type of prompt chain to run (default: %(default)s)'
    )

    return parser.parse_args()


def build_models():

    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    haiku_model = llm.get_model("claude-3-haiku")
    haiku_model.key = ANTHROPIC_API_KEY

    sonnet_model = llm.get_model("claude-3-sonnet")
    sonnet_model.key = ANTHROPIC_API_KEY

    opus_model = llm.get_model("claude-3-opus")
    opus_model.key = ANTHROPIC_API_KEY

    genai.configure(api_key=GEMINI_API_KEY)

    gemini_flash_model = genai.GenerativeModel('gemini-2.0-flash-exp')

    return haiku_model, sonnet_model, opus_model, gemini_flash_model


def coin_flip():
    return random.randint(0, 1)


def generate_response(model, prompt):
    """Helper function to handle different model types"""
    if hasattr(model, 'generate_content'):  # Gemini model
        response = model.generate_content(prompt)
        try:
            # Try to clean up the response by removing markdown code blocks if present
            text = response.text.replace('```json\n', '').replace('```', '')
            return text.strip()
        except Exception:
            return response.text
    elif hasattr(model, 'prompt'):  # LLM model
        response = model.prompt(prompt)
        return response.text()
    else:
        raise ValueError("Unsupported model type")


# ------ Prompt Chains

def prompt_chain_snowball(model):
    """
    Snowball prompt - start with a little information, that is developed over each prompt.
    Use Case
    - Blogs
    - Newsletters
    - Research
    - Summaries
    """

    base_information = "3 Unusual Use Cases for LLMs"

    # First prompt using generate_content()
    snowball_prompt_response_1 = generate_response(model,
        f"Generate a clickworthy title about this topic: '{base_information}'. Respond in JSON format {{title: 'title', topic: '{base_information}'}}"
    )

    print("Snowball #1: ", snowball_prompt_response_1)

    # Second prompt using generate_content() and accessing the previous response correctly
    snowball_prompt_response_2 = generate_response(model,
        f"Generate a compelling 3 section outline given this information: {snowball_prompt_response_1}. Respond in JSON format {{title: '<title>', topic: '<topic>', sections: ['<section1>', '<section2>', '<section3>']}}"
    )

    print("Snowball #2: ", snowball_prompt_response_2)

    # Third prompt
    snowball_prompt_response_3 = generate_response(model,
        f"Generate 1 paragraph of content for each section outline given this information: {snowball_prompt_response_2}. Respond in JSON format {{title: '<title>', topic: '<topic>', sections: ['<section1>', '<section2>', '<section3>'], content: ['<content1>', '<content2>', '<content3>']}}"
    )

    print("Snowball #3: ", snowball_prompt_response_3)

    # Final markdown formatting prompt
    snowball_markdown_prompt = generate_response(model,
        f"Generate a markdown formatted blog post given this information: {snowball_prompt_response_3}. Respond in JSON format {{markdown_blog: '<entire markdown blog post>'}}"
    )

    print("Final Snowball: ", snowball_markdown_prompt)

    with open("snowball_prompt_chain.txt", "w") as file:
        file.write(snowball_markdown_prompt)

    pass


def prompt_chain_workers(model):
    """
    Delegate different parts of your workload to individual prompt workers.
    Use Case
    - Research
    - Parallelization
    - Autocomplete
    - Divide and Conquer
    - Similar Tasks More Scalable
    Mermaid Diagram
    A[Start]
    B[Plan Prompt]
    C[Worker Prompt 1]
    D[Worker Prompt 2]
    E[Worker Prompt 3]
    F[Summary/Format Prompt]
    G[End]
    A --> B --> C
    B --> D
    B --> E
    E --> F
    C --> F
    D --> F
    F --> G
    """

    print("Generating function stubs...")

    # First worker: Generate stubs
    code_planner_prompt_response = generate_response(model,
        '''Create the function stubs for three functions:
        1. write_json_file(file_path: str, data: dict) -> None
        2. write_yml_file(file_path: str, data: dict) -> None
        3. write_toml_file(file_path: str, data: dict) -> None

        Include detailed docstrings with Args, Returns, Raises, and Usage examples.
        Respond in JSON format {function_stubs: ["def function1...", "def function2...", "def function3..."]}'''
    )

    try:
        function_stubs = json.loads(code_planner_prompt_response)["function_stubs"]
        print("\nGenerated stubs successfully!")
    except json.JSONDecodeError as e:
        print(f"Error parsing stubs: {e}")
        return

    # Second worker: Implement each stub
    implementations = []
    for i, stub in enumerate(function_stubs, 1):
        print(f"\nImplementing function {i}/3...")

        code_executor_prompt_response = generate_response(model,
            f'''Implement this function stub with proper error handling and imports:

{stub}

Respond in JSON format {{code: '<implementation>'}}'''
        )

        try:
            implementation = json.loads(code_executor_prompt_response)["code"]
            implementations.append(implementation)
            print(f"Function {i} implemented successfully!")
        except json.JSONDecodeError as e:
            print(f"Error parsing implementation {i}: {e}")
            continue

    if implementations:
        final_code = "\n\n".join(implementations)
        with open("files.py", "w") as file:
            file.write(final_code)
        print("\nAll implementations written to files.py")
    else:
        print("\nNo implementations were generated successfully")

    pass


def prompt_chain_fallback(model):
    """
    Fallback Prompt Chain - Tries cheaper/faster models first, falls back to more expensive/accurate models if needed.
    """
    def run_fallback_flow(evaluator_function, fallback_functions):
        print("\n🔄 Starting Fallback Chain...\n")

        for fallback_function, model_name, cost, speed in fallback_functions:
            print(f"🤖 Trying {model_name}")
            print(f"   💰 Cost: {cost}")
            print(f"   ⚡️ Speed: {speed}")

            response = fallback_function()
            print(f"\n📝 Response from {model_name}:")
            print(response)

            success = evaluator_function(response)

            if success:
                print(f"\n✅ {model_name} succeeded!")
                return True
            else:
                print(f"\n❌ {model_name} failed - falling back to next model...\n")

        print("❌ All fallback attempts failed")
        return False

    def run_code(code):
        """Simulated code execution with 50% success rate"""
        return coin_flip()

    function_generation_prompt = "Generate the solution in python given this function definition: 'def text_to_speech(text) -> Bytes'. Respond in JSON format {python_code: '<python code>'}"

    fallback_functions = [
        (
            lambda: generate_response(model, function_generation_prompt),
            "Claude 3 Haiku",
            "Low ($)",
            "Fast (0.5s)"
        ),
        (
            lambda: generate_response(model, function_generation_prompt),
            "Claude 3 Sonnet",
            "Medium ($$)",
            "Medium (1s)"
        ),
        (
            lambda: generate_response(model, function_generation_prompt),
            "Claude 3 Opus",
            "High ($$$)",
            "Slow (2s)"
        ),
    ]

    success = run_fallback_flow(run_code, fallback_functions)

    print(f"\n{'=' * 50}")
    print(f"Fallback Chain {'✅ Succeeded' if success else '❌ Failed'}")
    print(f"{'=' * 50}\n")


def prompt_chain_decision_maker(model):
    """
    Based on a decision from a prompt, run a different prompt chain.
    Use Case
    - Creative Direction
    - Dictate Flow Control
    - Decision Making
    - Dynamic Prompting
    - Multiple Prompts
    Mermaid Diagram
    A[Start]
    B[Decision Prompt]
    C[Prompt Chain 1]
    D[Prompt Chain 2]
    E[Prompt Chain 3]
    F[End]
    A --> B
    B --IF--> C --> F
    B --IF--> D --> F
    B --IF--> E --> F
    """

    live_feed = "The competitive landscape remains challenging, with some competitors engaging in aggressive pricing strategies."
    print(f"Analyzing Sentiment Of Latest Audio Clip: '{live_feed}'")

    sentiment_analysis_prompt_response = generate_response(model,
        f"Analyze the sentiment of the following text as either positive or negative: '{live_feed}'. Respond in JSON format {{\"sentiment\": \"positive\" | \"negative\"}}"
    )

    try:
        sentiment = json.loads(sentiment_analysis_prompt_response)["sentiment"]
        print(f"\nDetected Sentiment: {sentiment}")

        if sentiment == "negative":
            print("\nNegative sentiment detected - generating risk report...")
            # ... rest of the code
        else:
            print("\nPositive sentiment detected - generating opportunity report...")
            # ... rest of the code

    except json.JSONDecodeError as e:
        print(f"\nError parsing sentiment response: {sentiment_analysis_prompt_response}")
        print(f"JSON Error: {e}")
        return


def prompt_chain_plan_execute(model):
    """
    Plan Execute Prompt Chain
    Use Case
    - Tasks
    - Projects
    - Research
    - Coding
    Mermaid Diagram
    A[Start]
    B<Plan Prompt>
    C<Execute Prompt>
    D<End>
    A --> B --> C --> D
    """

    task = "Design the software architecture for an AI assistant that uses tts, llms, local sqlite. "

    plan_prompt_response = generate_response(model,
        f"Let's think step by step about how we would accomplish this task: '{task}'. Write all the steps, ideas, variables, mermaid diagrams, use cases, and examples concisely in markdown format. Respond in JSON format {{markdown_plan: '<plan>'}}"
    )

    print(plan_prompt_response)

    execute_prompt_response = generate_response(model,
        f"Create a detailed architecture document on how to execute this task '{task}' given this detailed plan {plan_prompt_response}.  Respond in JSON format {{architecture_document: '<document>'}}"
    )

    print(execute_prompt_response)

    # write the plan and execute to a file
    with open("plan_execute_prompt_chain.txt", "w") as file:
        file.write(execute_prompt_response)


def prompt_chain_human_in_the_loop(model, sonnet_model):
    """
    Human In The Loop Prompt Chain
    Use Case
    - Human In The Loop
    - Validation
    - Content Creation
    - Coding
    - Chat
    Mermaid Diagram
    A[Start]
    B[Initial Prompt]
    C[Human Feedback]
    D[Iterative Prompt]
    E[End]
    A --> B --> C --> D
    D --> C
    D --> E
    """
    topic = "Personal AI Assistants"
    prompt = f"Generate 5 ideas surrounding this topic: '{topic}'"
    result = generate_response(model, prompt)
    print(result)

    while True:
        user_input = input("Iterate on result or type 'done' to finish: ")
        if user_input.lower() == "done":
            break
        else:
            prompt += f"\n\n----------------\n\nPrevious result: {result}\n\n----------------\n\nIterate on the previous result and generate 5 more ideas based on this feedback: {user_input}"
            result = generate_response(sonnet_model, prompt)
            print(result + "\n\n----------------\n\n")

    pass


def prompt_chain_self_correct(model):
    """
    Self correct/review the output of a prompt.
    Use Case
    - Coding
    - Execution
    - Self Correct
    - Review
    - Iterate
    - Improve
    Mermaid Diagram
    A[Start]
    B[Prompt]
    C[Execute Output]
    D[Self Correct]
    E[End]
    A --> B --> C --> D --> E
    C --> E
    """

    def run_bash(command):
        print(f"Running command: {command}")
        if coin_flip() == 0:
            return "Mock error: command failed to execute properly"
        else:
            return "Command executed successfully"

    outcome = "list all files in the current directory"

    initial_response = generate_response(model,
        f"Generate a bash command that enables us to {outcome}. Respond with only the command."
    )
    print(f"Initial response: {initial_response}")

    # Run the generated command and check for errors
    result = run_bash(initial_response)

    if "error" in result.lower():

        print("Received error, running self-correction prompt")

        # If error, run self-correction prompt
        self_correct_response = generate_response(model,
            f"The following bash command was generated to {outcome}, but encountered an error when run:\n\nCommand: {initial_response}\nError: {result}\n\nPlease provide an updated bash command that will successfully {outcome}. Respond with only the updated command in JSON format {{command: '<command>'}}"
        )
        print(f"Self-corrected response: {self_correct_response}")

        # Run the self-corrected command
        run_bash(self_correct_response)

    else:
        print(f"Original command executed successfully: {result}")





def main():
    args = parse_args()

    # Build all models
    haiku_model, sonnet_model, opus_model, gemini_flash_model = build_models()

    # Select model based on argument
    model_map = {
        'gemini': gemini_flash_model,
        'haiku': haiku_model,
        'sonnet': sonnet_model,
        'opus': opus_model
    }

    selected_model = model_map[args.model]
    print(f"Using model: {args.model}")

    # Map of available prompt chains
    chain_map = {
        'snowball': prompt_chain_snowball,
        'workers': prompt_chain_workers,
        'fallback': prompt_chain_fallback,
        'decision': prompt_chain_decision_maker,
        'plan': prompt_chain_plan_execute,
        'human': lambda m: prompt_chain_human_in_the_loop(m, sonnet_model),
        'self-correct': prompt_chain_self_correct
    }

    # Run the selected prompt chain
    selected_chain = chain_map[args.chain]
    print(f"Running prompt chain: {args.chain}")
    selected_chain(selected_model)


if __name__ == "__main__":
    main()
