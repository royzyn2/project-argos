import os
import google.genai as genai
from dotenv import load_dotenv

# Attempt to load .env file if present
load_dotenv()

def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY is not set in environment or .env file.")
        print("Please set it via 'export GEMINI_API_KEY=...' or add it to a .env file.")
        return

    print(f"Found API Key: {api_key[:4]}...{api_key[-4:]}")
    
    try:
        client = genai.Client(api_key=api_key)
        print("Connecting to Gemini API...")
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents="Hello, are you working?"
        )
        
        if response.text:
            print("✅ Gemini API is working!")
            print(f"Response: {response.text}")
        else:
            print("⚠️ Received empty response.")
            
    except Exception as e:
        print(f"❌ Failed to connect to Gemini API: {e}")

if __name__ == "__main__":
    test_gemini()

