import os
import time
import google.generativeai as genai
from config.secrets_loader import get_secret

# 1. Configure
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found.")
    exit(1)

genai.configure(api_key=api_key)

model_name = "gemini-2.5-pro"
print(f"--- Testing {model_name} ---")

try:
    model = genai.GenerativeModel(model_name)
    
    # 2. Simple Test
    print("1. Sending 'Hello'...")
    start = time.time()
    response = model.generate_content("Hello, are you Gemini 2.5 Pro?")
    duration = time.time() - start
    print(f"Response ({duration:.2f}s): {response.text}")
    
    # 3. Load Test (Simulation)
    print("\n2. Sending Large Payload (10k chars)...")
    dummy_transcript = "This is a test transcript. " * 500 # ~13k chars
    prompt = f"Analyze this transcript: {dummy_transcript}. Summarize in one sentence."
    
    start = time.time()
    response = model.generate_content(prompt)
    duration = time.time() - start
    print(f"Response ({duration:.2f}s): {response.text}")
    
    print("\n--- SUCCESS ---")

except Exception as e:
    print(f"\n--- FAILED ---")
    print(f"Error: {e}")

