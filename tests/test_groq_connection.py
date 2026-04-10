"""Test Groq API connectivity and basic response."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from groq import Groq


def test_connection():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key or api_key == "your_groq_api_key_here":
        print("Error: GROQ_API_KEY is not set or is still the placeholder.")
        return

    client = Groq(api_key=api_key)

    test_prompts = [
        "Respond with exactly 'Connection Successful.'",
        "Explain in one sentence why a restaurant recommendation system needs an LLM.",
        "What is the capital of France?",
        "Give me a 3-word slogan for an AI food app.",
    ]

    print(f"--- Starting {len(test_prompts)} tests ---")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nTest Case {i}: \"{prompt}\"")
        try:
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
            )
            print(f"Response: {completion.choices[0].message.content}")
        except Exception as e:
            print(f"Error during Test Case {i}: {e}")


if __name__ == "__main__":
    test_connection()
