from compilation_engine import CompilationEngine
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

def compilation_engine_test(file: str, content: str) -> None:
    output_file = file.replace(".jack", ".xml")
    engine = CompilationEngine(content)
    engine.compile()
    with open(output_file, 'w') as f:
        for line in engine.output:
            f.write(line + "\r\n")

def compile(file: str, content: str) -> None:
    xml_output_file = file.replace(".jack", ".xml")
    vm_output_file = file.replace(".jack", ".vm")
    engine = CompilationEngine(content)
    engine.compile()
    with open(xml_output_file, 'w') as f:
        for line in engine.output:
            f.write(line + "\r\n")
    engine.vm_writer.write(vm_output_file)

def process_files(jack_files: list[str], test_tokenizer: bool, test_compilation_engine: bool):
    for file in jack_files:
        print(f"Processing file: {file}")
        with open(file, 'r') as f:
            content = f.read()
        
        if test_tokenizer:
            print("Running tokenizer test mode")
            tokenizer_test(file, content)
        elif test_compilation_engine:
            print("Running compilation engine test mode")
            compilation_engine_test(file, content)
        else:
            print("Compile mode")
            compile(file, content)

def main():
    parser = argparse.ArgumentParser(description='Compile Jack files')
    parser.add_argument('--test_tokenizer', action='store_true',
                      help='run in tokenizer test mode')
    parser.add_argument('--test_compilation_engine', action='store_true',
                      help='run in compilation engine test mode')
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

    process_files(jack_files, args.test_tokenizer, args.test_compilation_engine)

if __name__ == "__main__":
    main()

