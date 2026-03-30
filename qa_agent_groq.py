import os
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

# Carrega as chaves do arquivo .env
load_dotenv()

def save_report(report_text):
    """Saves the generated report to a markdown file with persistence check."""
    folder = "bug_reports"
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bug_report_groq_{timestamp}.md"
    filepath = os.path.join(folder, filename)
    
    try:
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(report_text)
        return filepath
    except Exception as e:
        print(f"⚠️ Failed to save file: {e}")
        return None

# --- CONFIG & VALIDATION ---
GROQ_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_KEY:
    print("❌ CRITICAL ERROR: GROQ_API_KEY not found in .env file!")
    exit()

client = Groq(api_key=GROQ_KEY)

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

def main():
    print("🚀 QA Agent (GROQ VERSION) Online!")
    print("Tip: type 'exit' to close.")

    try:
        while True:
            print("\n" + "=" * 50)
            user_input = input("Describe the bug (or raw logs): ").strip()

            # 1. Check for exit first
            if user_input.lower() in ['exit', 'quit', 'sair']:
                print("Closing Agent. Happy testing!")
                break
            
            # 2. Check for empty or too short input
            if len(user_input) < 5:
                print("⚠️ Please provide more details (minimum 5 characters).")
                continue
            
            print("🤖 Analyzing with Llama-3 (Groq)...")
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        {"role": "user", "content": user_input}
                    ]
                )
                report = completion.choices[0].message.content
                
                print(f"\n--- GENERATED BUG REPORT ---\n{report}")
                
                path = save_report(report)
                if path:
                    print(f"\n📁 File saved: {path}")
                    
            except Exception as e:
                print(f"❌ API Error: {e}")

    except KeyboardInterrupt:
        print("\n\n⚠️ Process interrupted by user. Goodbye!")

if __name__ == "__main__":
    main()