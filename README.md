# Transcript Analysis Tool

This tool uses OpenAI's GPT-4o-mini model to analyze transcripts and extract essential information, focusing on key concepts, best practices, tips, and code snippets.

## Setup

1. Ensure you have Python 3.7+ installed.
2. Install the required packages:   ```
   pip install -r requirements.txt   ```
3. Create a `.env.local` file in the `transcript_analysis_tool` directory with your OpenAI API key:   ```
   OPENAI_API_KEY=your_api_key_here   ```

## Usage

Run the script from the command line:

python transcript_analyzer.py

You can optionally provide the path to the transcript file as an argument:

python transcript_analyzer.py path/to/your/transcript.txt

If you don't provide a file path, the script will prompt you to enter one.

For example:
python transcript_analyzer.py
Please enter the full path to the transcript file: C:\Users\YourName\Documents\transcripts\Essential_AI_Coding_Fundamentals.txt

The script will:
1. Analyze the specified transcript file.
2. Extract essential information, including key concepts, best practices, tips, and code snippets.
3. Print the extracted information to the console.
4. Save the extracted information as a JSON file in the `corrected_transcripts` folder within the project directory. The filename will have "CORRECTED_" prepended and "_essential_info" appended to the original filename.

## Customization

You can modify the `analyze_transcript()` function to extract different types of information or adjust the analysis parameters. The current version uses the "gpt-4o-mini" model, which may not be a standard OpenAI model. If you encounter issues, you may need to change the model to a standard one like "gpt-3.5-turbo" or "gpt-4".

## Using the Extracted Information

The extracted information is structured in a way that makes it easy to use in AI prompts. You can load the JSON file from the `corrected_transcripts` folder and use its contents to create focused, information-rich prompts for various AI applications.
