import json
import random
import tqdm
import os
from src import BUG_TYPES, BUG_CONDITIONS, BUG_NUM
from leetcode_oj import LeetCodeTester
from src import BugGenerator
from src import GPT4Responser

WORK_DIR = "benchmark_construction"
LANGS = ["python3", "java", "cpp"]
TESTER = LeetCodeTester()
responser = GPT4Responser()
GENERATOR = BugGenerator(responser)


def load_cases(lang: str) -> list:
    with open(f"{WORK_DIR}/cases/{lang}.json") as f:
        return json.load(f)


def save_buggy_cases(lang: str, buggy_cases: list, bug_type: str) -> None:
    with open(f"{WORK_DIR}/bugs/{lang}_{bug_type}.json", "w") as f:
        json.dump(buggy_cases, f, indent=4)


def generate_bug_cases(lang: str, bug_type: str, cases: list, implant_condition, bug_num: int) -> list:
    res = []
    filtered_cases = [case for case in cases if implant_condition(case)]
    sampled_cases = random.sample(filtered_cases, min(bug_num, len(filtered_cases)))
    for case in tqdm.tqdm(sampled_cases, desc=f"{lang} {bug_type}"):

        code = case['oracle_code']
        bug, explanation = GENERATOR.generate_bug(code=code, lang=lang, bug_type=bug_type)
        rw, res_dict = TESTER.test(code=bug, language=lang, task_id=case['slug'])

        if not rw:
            case['buggy_code'] = bug
            case['explanations'] = explanation
            res.append(case)
    return res


def main(lang: str):
    cases = load_cases(lang=lang)

    for bug_type in BUG_TYPES[lang]:
        save_dir = f"{WORK_DIR}/bugs/{lang}_{bug_type}.json"
        # if exists this path, skip
        if os.path.exists(save_dir):
            print(f"{lang} {bug_type} exists")
            continue
        condition = BUG_CONDITIONS[lang][bug_type]
        bug_num = BUG_NUM[bug_type]
        buggy_cases = generate_bug_cases(lang=lang,
                                         bug_type=bug_type,
                                         cases=cases,
                                         implant_condition=condition,
                                         bug_num=bug_num)
        save_buggy_cases(lang=lang, buggy_cases=buggy_cases, bug_type=bug_type)


if __name__ == '__main__':

    for the_lang in LANGS:
        main(the_lang)
