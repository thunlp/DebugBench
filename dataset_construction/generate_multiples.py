import os
import json
import tqdm
import random
import difflib
from itertools import combinations

WORK_DIR = "benchmark_construction"
CASE_DIR = f"{WORK_DIR}/cases"
BUG_DIR = f"{WORK_DIR}/cleaned_bugs"


def merge(s1, s2, s3):
    diff1 = difflib.ndiff(s1, s2)
    diff2 = difflib.ndiff(s1, s3)
    patch1 = list(diff1)
    patch2 = list(diff2)

    new_patch = []
    idx1 = 0
    idx2 = 0
    while idx1 != len(patch1) or idx2 != len(patch2):

        if idx1 < len(patch1) and idx2 < len(patch2):

            if patch1[idx1][0] == '+' and patch2[idx2][0] == '+' and patch1[idx1] != patch2[idx2]:
                raise Exception("delta conflict!")

            elif patch1[idx1][0] == '+' and patch2[idx2][0] == '+':
                new_patch.append(patch1[idx1])
                idx1 += 1
                idx2 += 1

            elif patch1[idx1][0] == '+':
                new_patch.append(patch1[idx1])
                idx1 += 1

            elif patch2[idx2][0] == '+':
                new_patch.append(patch2[idx2])
                idx2 += 1

            else:
                assert patch1[idx1][1:] == patch2[idx2][1:]
                if patch1[idx1][0] == '-' or patch2[idx2][0] == '-':
                    new_patch.append('-' + patch1[idx1][1:])
                else:
                    new_patch.append(patch1[idx1])
                idx1 += 1
                idx2 += 1

        else:
            if idx1 < len(patch1):
                new_patch.append(patch1[idx1])
                idx1 += 1
            else:
                new_patch.append(patch2[idx2])
                idx2 += 1

    return "".join(difflib.restore(new_patch, 2))


def load_cases(lang: str) -> list:
    with open(f"{CASE_DIR}/{lang}.json") as f:
        return json.load(f)


def load_bugs(lang: str) -> dict:
    bugs = {}
    json_files = [file for file in os.listdir(BUG_DIR) if lang in file]
    for file_name in json_files:
        with open(os.path.join(BUG_DIR, file_name)) as f:
            data = json.load(f)
            bug_type = file_name[:file_name.find('.json')].split('_')[1]
            bugs[bug_type] = data
    return bugs


def attach_bugs(cases: list, lang: str) -> None:
    bugs = load_bugs(lang)
    for case in tqdm.tqdm(cases):
        case['generated_bugs'] = []
        for bug_type, bug_data in bugs.items():
            for bug in bug_data:
                if case['oracle_code'] == bug['oracle_code']:
                    case['generated_bugs'].append({"type": bug_type, "code": bug['buggy_code']})


def merge_bugs(cases: list) -> None:
    def harvest_double_bugs(oracle_code: str, parallel_bugs: list) -> list:
        buggy_code = []
        for comb in combinations(parallel_bugs, 2):
            try:
                merge_code = {'type': [comb[0]['type'], comb[1]['type']],
                              'code': merge(oracle_code, comb[0]['code'], comb[1]['code'])}
                buggy_code.append(merge_code)
            except:
                pass
        return buggy_code

    def harvest_triple_bugs(oracle_code: str, parallel_bugs: list) -> list:
        buggy_code = []
        for comb in combinations(parallel_bugs, 3):
            try:
                code_1 = merge(oracle_code, comb[0]['code'], comb[1]['code'])
                code_2 = merge(oracle_code, code_1, comb[2]['code'])
                merge_code = {'type': [comb[0]['type'], comb[1]['type'], comb[2]['type']],
                              'code': code_2}
                buggy_code.append(merge_code)
            except:
                pass
        return buggy_code

    def harvest_quadruple_bugs(oracle_code: str, parallel_bugs: list) -> list:
        buggy_code = []
        for comb in combinations(parallel_bugs, 4):
            try:
                code_1 = merge(oracle_code, comb[0]['code'], comb[1]['code'])
                code_2 = merge(oracle_code, code_1, comb[2]['code'])
                code_3 = merge(oracle_code, code_2, comb[3]['code'])
                merge_code = {'type': [comb[0]['type'], comb[1]['type'], comb[2]['type'], comb[3]['type']],
                              'code': code_3}
                buggy_code.append(merge_code)
            except:
                print("conflict!")
        return buggy_code

    for case in tqdm.tqdm(cases):
        oracle_code = case['oracle_code']
        parallel_bugs = case['generated_bugs']

        if len(parallel_bugs) >= 2:
            res = harvest_double_bugs(oracle_code, parallel_bugs)
            if res:
                case['double_bug'] = res

        if len(parallel_bugs) >= 3:
            res = harvest_triple_bugs(oracle_code, parallel_bugs)
            if res:
                case['triple_bug'] = res

        if len(parallel_bugs) >= 4:
            res = harvest_quadruple_bugs(oracle_code, parallel_bugs)
            if res:
                case['quadruple_bug'] = res


def save_files(cases: list, lang: str) -> None:
    def extract_double_bugs(case: dict) -> list:
        res = []
        if 'double_bug' in case:
            for bug in case['double_bug']:
                bug = {
                    "slug": case['slug'],
                    "description": case['description'],
                    "examples": case['examples'],
                    "constrains": case['constrains'],
                    "oracle_code": case['oracle_code'],
                    "content": case['content'],
                    "level": case['level'],
                    "type": bug['type'],
                    "buggy_code": bug['code']
                }
                res.append(bug)
        return res

    def extract_triple_bugs(case: dict) -> list:
        res = []
        if 'triple_bug' in case:
            for bug in case['triple_bug']:
                bug = {
                    "slug": case['slug'],
                    "description": case['description'],
                    "examples": case['examples'],
                    "constrains": case['constrains'],
                    "oracle_code": case['oracle_code'],
                    "content": case['content'],
                    "level": case['level'],
                    "type": bug['type'],
                    "buggy_code": bug['code']
                }
                res.append(bug)
        return res

    def extract_quadruple_bugs(case: dict) -> list:
        res = []
        if 'quadruple_bug' in case:
            for bug in case['quadruple_bug']:
                bug = {
                    "slug": case['slug'],
                    "description": case['description'],
                    "examples": case['examples'],
                    "constrains": case['constrains'],
                    "oracle_code": case['oracle_code'],
                    "content": case['content'],
                    "level": case['level'],
                    "type": bug['type'],
                    "buggy_code": bug['code']
                }
                res.append(bug)
        return res

    double_bugs = []
    triple_bugs = []
    quadruple_bugs = []
    for case in cases:
        double_bugs += extract_double_bugs(case)
        triple_bugs += extract_triple_bugs(case)
        quadruple_bugs += extract_quadruple_bugs(case)

    with open(f"{BUG_DIR}/{lang}_double.json", 'w') as f:
        json.dump(random.sample(double_bugs, min(250, len(double_bugs))), f, indent=4)
    with open(f"{BUG_DIR}/{lang}_triple.json", 'w') as f:
        json.dump(random.sample(triple_bugs, min(250, len(triple_bugs))), f, indent=4)
    with open(f"{BUG_DIR}/{lang}_quadruple.json", 'w') as f:
        json.dump(random.sample(quadruple_bugs, min(250, len(quadruple_bugs))), f, indent=4)


def main():
    for lang in ("java", "cpp", "python3"):
        cases = load_cases(lang)
        attach_bugs(cases, lang)
        merge_bugs(cases)
        save_files(cases, lang)


if __name__ == '__main__':
    main()
