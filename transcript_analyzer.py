import os
import sys
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv

# Add the parent directory to sys.path to allow importing from youtube-transcriber
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables from the local .env.local file
load_dotenv('.env.local')

# Set up OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def analyze_transcript(transcript):
    """
    Analyze the transcript using OpenAI's function calling and text generation.
    """
    functions = [
        {
            "name": "extract_essential_information",
            "description": "Extract essential information, best practices, and tips from the transcript",
            "parameters": {
                "type": "object",
                "properties": {
                    "key_concepts": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of key concepts discussed in the transcript"
                    },
                    "best_practices": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of best practices mentioned in the transcript"
                    },
                    "tips": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of practical tips provided in the transcript"
                    },
                    "code_snippets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "language": {"type": "string"},
                                "code": {"type": "string"},
                                "explanation": {"type": "string"}
                            }
                        },
                        "description": "List of important code snippets with their explanations"
                    }
                },
                "required": ["key_concepts", "best_practices", "tips", "code_snippets"]
            }
        }
    ]

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Note: This model name might not be recognized by the API
        messages=[
            {"role": "system", "content": "You are an AI assistant that extracts essential information from transcripts, focusing on key concepts, best practices, tips, and code snippets. You have expertise in programming, AI, and software development."},
            {"role": "user", "content": f"""
            Analyze the following transcript and extract the most essential information, focusing on programming, AI, and software development topics. The transcript is likely from a video or presentation about coding practices, AI tools, or software development techniques.

            1. Key concepts: Identify and list the main ideas or concepts discussed. For example:
               - "Prompt engineering in AI"
               - "Version control best practices"
               - "Efficient code refactoring techniques"

            2. Best practices: Extract any mentioned best practices or recommended approaches. For example:
               - "Always use meaningful variable names for better code readability"
               - "Implement continuous integration for smoother development workflows"
               - "Regularly update and test AI models to maintain accuracy"

            3. Tips: Collect practical tips or advice given in the transcript. For example:
               - "Use keyboard shortcuts in your IDE to speed up coding"
               - "Leverage AI-powered code completion tools to increase productivity"
               - "Break down complex problems into smaller, manageable tasks"

            4. Code snippets: If present, extract important code examples with their explanations. Include the programming language used. For example:
               {{
                 "language": "Python",
                 "code": "def greet(name):\n    return f'Hello, {{name}}!'",
                 "explanation": "This function demonstrates f-string usage in Python for string formatting."
               }}

            Present the information in a concise, structured format suitable for use in AI prompts.
            Omit any unnecessary details or repetitive information.
            If certain categories are not applicable or not present in the transcript, you may leave them empty.

            Transcript: {transcript}
            """}
        ],
        functions=functions,
        function_call={"name": "extract_essential_information"}
    )

    return json.loads(completion.choices[0].message.function_call.arguments)

def process_transcript(file_path):
    """
    Process a transcript file and save the extracted information.
    """
    try:
        with open(file_path, 'r') as file:
            transcript = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except IOError:
        print(f"Error: Could not read the file '{file_path}'.")
        return None

    result = analyze_transcript(transcript)

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'corrected_transcripts')
    os.makedirs(output_dir, exist_ok=True)

    file_name = os.path.basename(file_path)
    output_path = os.path.join(output_dir, f"CORRECTED_{file_name.split('.')[0]}_essential_info.json")
    with open(output_path, 'w') as file:
        json.dump(result, file, indent=2)

    return output_path

def main():
    parser = argparse.ArgumentParser(description="Analyze a transcript file and extract essential information.")
    parser.add_argument("file_path", nargs='?', help="Path to the transcript file to analyze")
    args = parser.parse_args()

    if args.file_path is None:
        args.file_path = input("Please enter the full path to the transcript file: ")

    output_path = process_transcript(args.file_path)
    if output_path:
        print(f"\nEssential information saved to: {output_path}")

if __name__ == "__main__":
    main()
