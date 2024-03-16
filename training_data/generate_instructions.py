from openai import OpenAI
import json


def load_config(file_path='config.json'):
    """Load configuration from a JSON file."""
    with open(file_path, 'r') as file:
        config = json.load(file)
    return config


def create_openai_client(api_key):
    """Create an OpenAI client using the provided API key."""
    return OpenAI(api_key=api_key)


def read_fortran_code_from_jsonl(file_path):
    """Yield Fortran code strings from a JSONL file."""
    with open(file_path, 'r') as file:
        for line in file:
            yield json.loads(line)['text']


def save_to_jsonl(data, file_path):
    """Save data to a JSONL file, appending each new entry."""
    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write('\n')


def generate_instructions(client, prompt_prepend, fortran_code, output_file):
    """Generate instructions and save results to JSONL file."""
    chat_content = prompt_prepend + fortran_code
    gpt_result = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": chat_content,
            }
        ],
        model="gpt-3.5-turbo",
        temperature=0.2
    )
    result_content = gpt_result.choices[0].message.content
    data = {"prompt": result_content, "completion": fortran_code}
    save_to_jsonl(data, output_file)
    return result_content


def count_lines_in_file(file_path):
    """Count the number of lines in a file."""
    try:
        with open(file_path, 'r') as file:
            return sum(1 for line in file)
    except FileNotFoundError:
        return 0


def main():
    config = load_config()
    client = create_openai_client(config['openai_api_key'])
    output_file = config['output_file']
    input_line_count = count_lines_in_file(config['dataset_file'])

    output_line_count = count_lines_in_file(output_file)
    if output_line_count >= input_line_count:
        print("Output file contains as many or more entries than input file. No further action needed or possible error in files.")
        exit(0)

    start_line = output_line_count + 1

    with open(config['prompt_file'], 'r') as file:
        prompt_prepend = file.read()

    count = 0
    for i, fortran_code in enumerate(read_fortran_code_from_jsonl(config['dataset_file']), start=1):
        if i % 10 == 0:
            print(
                f"\nLine {str(i).zfill(6)} of {str(input_line_count).zfill(6)}: ", end="", flush=True)

        if i >= start_line and len(fortran_code) <= 25000:
            generate_instructions(client, prompt_prepend,
                                  fortran_code, output_file)
            print(".", end="", flush=True)
            count += 1

    print("\nProcessing complete.")


if __name__ == '__main__':
    main()
