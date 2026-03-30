from google import genai
import os
from datetime import datetime

# File Resistence
def save_report(report_text):
    """Saves the generated report to a markdown file."""
    folder = "bug_reports"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bug_report_{timestamp}.md"
    filepath = os.path.join(folder, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(report_text)
        return filepath
    except Exception as e:
        print(f"⚠️ Failed to save file: {e}")
        return None

# Configurations
API_KEY = os.getenv("GEMINI_API_KEY")
# List of models for fallback (resilience)
MODELS_PRIORITY = ["gemini-2.0-flash-lite", "gemini-1.5-flash", "gemini-1.5-flash-8b"]

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

# Core Functions
def initialize_agent():
    """Initializes the GenAI Client with security checks."""
    if not API_KEY:
        raise ValueError ("CRITICAL ERROR: GEMINI_API_KEY not found in environment variables.")
    return genai.Client(api_key=API_KEY)

def generate_bug_report(client, raw_content):
    """Processes the raw input and returns a structured report."""
    config = {'system_instruction': SYSTEM_INSTRUCTION}

    for model_name in MODELS_PRIORITY:
        try:
            print(f"🤖 Trying model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                config=config,
                contents=raw_content
            )
            return response.text, model_name
        
        except Exception as e:
            print(f"⚠️ {model_name} failed. Moving to next candidate...")
            continue
    
    return "All AI models are currently unavaliable. Please try again later.", "None"
    
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
            report, model_used = generate_bug_report(client, user_input)

            if model_used != "None":
                print(f"✅ Generated successfully using: {model_used}")
                print("\n--- GENERATED BUG REPORT ---")
                print(report)
                print("=" * 50)

                path = save_report(report)
                if path:
                    print(f"Report saved to: {path}")
                
            else:
                print(f"\n❌ {report}")

            print("=" * 50)

    except Exception as error:
        print(f"Application Error: {error}")

if __name__ == "__main__":
    main()

