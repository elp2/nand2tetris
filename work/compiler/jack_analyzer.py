import JackTokenizer
import sys
import os
import argparse

def process_files(jack_files: list[str], test_tokenizer: bool):
    for file in jack_files:
        print(f"Processing file: {file}")

        
        if test_tokenizer:
            print("Running tokenizer test mode")
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

