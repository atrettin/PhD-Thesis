import argparse
import re

def convert_file(input_file_path, output_file_path=None):
    if output_file_path is None:
        output_file_path = input_file_path
    with open(input_file_path, 'r') as file:
        text = file.read()

    # split the text into lines
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('%') or ('\\\\' in line) or line.endswith('}'):
            new_lines.append(line)
        else:
            sentences = re.split(r'(?<=[.!?])\s(?=(?:[^\{]*\{[^\{]*\})*[^\{]*$)', line)
            new_lines.extend(sentences)

    # write the sentences to a new file, each on its own line
    with open(output_file_path, 'w') as file:
        file.write('\n'.join(new_lines))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a file so that each sentence is on its own line')
    parser.add_argument('input_file', help='the file to be converted')
    parser.add_argument('output_file', nargs='?', help='the output file, defaults to be the same as the input file')
    args = parser.parse_args()

    convert_file(args.input_file, args.output_file)
