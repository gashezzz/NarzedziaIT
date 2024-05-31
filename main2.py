import sys
import json
import yaml
import xmltodict
import argparse

def convert(input_path, output_path):
    with open(input_path, 'r') as file:
        if input_path.endswith('.json'):
            data = json.load(file)
        elif input_path.endswith('.xml'):
            data = xmltodict.parse(file.read())
        elif input_path.endswith('.yaml') or input_path.endswith('.yml'):
            data = yaml.safe_load(file)
        else:
            raise ValueError('Unsupported input file format')

    with open(output_path, 'w') as file:
        if output_path.endswith('.json'):
            json.dump(data, file, indent=4)
        elif output_path.endswith('.xml'):
            xml_str = xmltodict.unparse(data, pretty=True)
            file.write(xml_str)
        elif output_path.endswith('.yaml') or output_path.endswith('.yml'):
            yaml.dump(data, file)
        else:
            raise ValueError('Unsupported output file format')

def main():
    parser = argparse.ArgumentParser(description="Convert files between JSON, XML, and YAML formats.")
    parser.add_argument('input_path', help="Path to the input file")
    parser.add_argument('output_path', help="Path to the output file")
    args = parser.parse_args()

    try:
        convert(args.input_path, args.output_path)
        print("File converted successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
