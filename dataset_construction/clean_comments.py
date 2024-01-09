import os
import json

WORK_DIR = "benchmark_construction"
SRC_DIR = f"{WORK_DIR}/bugs"
TGT_DIR = f"{WORK_DIR}/cleaned_raw_bugs"


def load_files():
    files = os.listdir(SRC_DIR)
    files = [f"{SRC_DIR}/{file}" for file in files]
    return files


def clean_code(original_code: str, generated_code: str, lang: str):
    modified_code = generated_code

    # find different lines
    original_lines = original_code.split('\n')
    generated_lines = generated_code.split('\n')
    different_lines = [line for line in generated_lines if line not in original_lines]

    # assign signs
    assert lang in ('python3', 'cpp', 'java')
    comment_mark = '#' if lang == 'python3' else '//'

    # modify lines
    for line in different_lines:
        if comment_mark in line:
            new_line = line[: line.find(comment_mark)]
            modified_code = modified_code.replace(line, new_line)
    return modified_code


def clean_datum(datum: dict, lang: str):
    original_code = datum['oracle_code']
    generated_code = datum['buggy_code']
    new_generated_code = clean_code(original_code, generated_code, lang)
    datum['buggy_code'] = new_generated_code
    return datum


def clean_data(data: dict, lang: str):
    new_data = []
    for datum in data:
        new_datum = clean_datum(datum, lang)
        new_data.append(new_datum)
    return new_data


def clean_file(file_path: str):
    input_path = file_path
    lang = input_path.split('/')[-1].split('_')[0]
    output_path = input_path.replace(SRC_DIR, TGT_DIR)

    with open(input_path, 'r') as f:
        data = json.load(f)

    cleaned_data = clean_data(data, lang)

    with open(output_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)


def main():
    files = load_files()
    for file in files:
        clean_file(file)


if __name__ == "__main__":
    main()
