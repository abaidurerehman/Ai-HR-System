from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv('GEMINI_API_KEY')

if key:
    print(f"✅ Key found")
    print(f"First 15 chars: {key[:15]}")
    print(f"Length: {len(key)} characters")
    print(f"Starts with 'AIza': {key.startswith('AIza')}")
else:
    print("❌ Key NOT found")