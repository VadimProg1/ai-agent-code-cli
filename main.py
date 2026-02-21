import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt 
from functions.available_functions import available_functions
from functions.call_function import call_function

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
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, user_input.verbose)
            if function_call_result.parts == None or len(function_call_result.parts) == 0:
                raise Exception("Parts is empty")
            result_parts = function_call_result.parts
            if result_parts[0].function_response == None or result_parts[0].function_response.response == None:
                raise Exception("Function response is empty")
            function_results = result_parts[0]
            if user_input.verbose:
                print(f"-> {result_parts[0].function_response.response}")
    else:
        print(f"Response:\n{response.text}")
    

if __name__ == "__main__":
    main()
