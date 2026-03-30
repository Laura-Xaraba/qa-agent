from google import genai
import os

# Configurations
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-2.0-flash-lite"

# System Instruction 
SYSTEM_INSTRUCTION = """
You are a Senior QA Analyst Agent specialized in bug triaging.
Your task is to receive informal bug descriptions and transform them into professional Bug Reports.

Output Format (Markdown):
- **Title**: Clear and Objective
- **Severity**: (Critical, High, Medium, Low)
- **Steps to Reproduce**: (Numbered list)
- **Expected vs. Actual Result**: (Comparison)
- **Possible Root Cause**: (Technical hypothesis)
"""

def initialize_agent():
    """Initializes the GenAI Client with security checks."""
    if not API_KEY:
        raise ValueError ("CRITICAL ERROR: GEMINI_API_KEY not found in environment variables.")
    return genai.Client(api_key=API_KEY)

def generate_bug_report(client, raw_content):
    """Processes the raw input and returns a structured report."""
    config = {'system_instruction': SYSTEM_INSTRUCTION}

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=config,
            contents=raw_content
        )
        return response.text
    except Exception as e:
        return f"Error processing report: {str(e)}"
    
# Main Execution Loop
def main():
    try:
        client = initialize_agent()
        print("QA Agent Online & Secure!")
        print("Tip: type 'exit' to close the program.")

        while True:
            print("\n" + "=" * 50)
            user_input = input("Describe the bug (or raw logs): ").strip()

            if user_input.lower() in ['exit', 'quit', 'sair']:
                print("Closing Agent. Happy testing!")
                break

            if not user_input:
                continue

            print("Analyzing and structuring data...")
            report = generate_bug_report(client, user_input)

            print("\n--- GENERATED BUG REPORT ---")
            print(report)
            print("=" * 50)

    except Exception as error:
        print(f"Application Error: {error}")

if __name__ == "__main__":
    main()

