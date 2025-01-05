from jack_tokenizer import JackTokenizer, JackToken

import argparse
import sys
import os

def tokenizer_test(file: str, content: str) -> None:
    output_file = file.replace(".jack", "T.xml")
    with open(output_file, 'w') as f:
        f.write("<tokens>\r\n")
        tokenizer = JackTokenizer(content)
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            token = tokenizer.get_current_token()
            f.write(token.xml_str() + "\r\n")
        f.write("</tokens>\r\n")

def process_files(jack_files: list[str], test_tokenizer: bool):
    for file in jack_files:
        print(f"Processing file: {file}")
        with open(file, 'r') as f:
            content = f.read()
        
        tokenizer = JackTokenizer(content)
        
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            current_token = tokenizer.get_current_token()
            print(current_token)
        
        if test_tokenizer:
            print("Running tokenizer test mode")
            tokenizer_test(file, content)
            # Add tokenizer test code here
        else:
            print("Running analyzer mode")
            # Add analyzer code here

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Analyze Jack files')
    parser.add_argument('--test_tokenizer', action='store_true',
                      help='run in tokenizer test mode')
    parser.add_argument('input_path',
                      help='input .jack file or directory containing .jack files')
    
    args = parser.parse_args()
    jack_files = []

    if os.path.isdir(args.input_path):
        # Get all .jack files in directory
        for file in os.listdir(args.input_path):
            if file.endswith(".jack"):
                jack_files.append(os.path.join(args.input_path, file))
        if not jack_files:
            print(f"Error: No .jack files found in directory {args.input_path}")
            sys.exit(1)
    else:
        # Single file
        if not args.input_path.endswith(".jack"):
            print("Error: Input file must be a .jack file")
            sys.exit(1)
        jack_files = [args.input_path]

    process_files(jack_files, args.test_tokenizer)

if __name__ == "__main__":
    main()

