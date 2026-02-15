import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt 
from functions.available_functions import available_functions

def get_llm_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("API key not found!")
    return genai.Client(api_key=api_key)

def setup_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser

def print_metadata(user_input, response):
    prompt_tokens_count = response.usage_metadata.prompt_token_count
    candidates_tokens_count = response.usage_metadata.candidates_token_count
    print(f"User prompt: {user_input.prompt}")
    print(f"Prompt tokens: {prompt_tokens_count}")
    print(f"Response tokens: {candidates_tokens_count}")
    

def main():
    model_name = "gemini-2.5-flash"
    client = get_llm_client()
    user_input = setup_parser().parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=user_input.prompt)])]
    
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.usage_metadata == None:
        raise RuntimeError("Usage metadata from response not found!")
    
    if user_input.verbose:
        print_metadata(user_input, response)

    if response.function_calls != None or len(response.function_calls) > 0:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Response:\n{response.text}")
    

if __name__ == "__main__":
    main()
