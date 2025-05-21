import os
from openai import OpenAI
from dotenv import load_dotenv  # Used to load environment variables from .env file

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI client with your API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to query the model
def chat_with_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

# Test example
if __name__ == "__main__":
    print(chat_with_openai("What is Process Mining?"))