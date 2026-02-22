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
    

def call_llm(messages):
    v3model_name = "gemini-3-flash-preview"
    v2model_name = "gemini-2.5-flash"
    client = get_llm_client()
    response = client.models.generate_content(
        model=v2model_name,
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )
    if response.usage_metadata == None:
        raise RuntimeError("Usage metadata from response not found!")
    return response

def use_functions(response, user_input):
    if response.function_calls != None and len(response.function_calls) > 0:
        function_results = []
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, user_input.verbose)
            if function_call_result.parts == None or len(function_call_result.parts) == 0:
                raise Exception("Parts is empty")
            result_parts = function_call_result.parts
            if result_parts[0].function_response == None or result_parts[0].function_response.response == None:
                raise Exception("Function response is empty")
            function_results = result_parts
            if user_input.verbose:
                print(f"-> {result_parts[0].function_response.response}")
        return function_results
    else:
        print(f"Final response:\n{response.text}")

def main():
    user_input = setup_parser().parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=user_input.prompt)])]
    had_final_response = False
    for _ in range(10):
        response = call_llm(messages)
    
        if user_input.verbose:
            print_metadata(user_input, response)

        for candidate in response.candidates:
            messages.append(candidate)

        functions_call_result = use_functions(response, user_input)
        if functions_call_result == None:
            had_final_response = True
            break
        messages.append(types.Content(role="user", parts=functions_call_result))
    if not had_final_response:
        exit(1)

if __name__ == "__main__":
    main()
