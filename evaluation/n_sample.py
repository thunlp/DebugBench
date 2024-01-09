import os
import sys
import json
import tqdm

from leetcode_oj import LeetCodeTester
from debugger import GPT4Responser, TurboResponser, IODebugger

SETTING = "n_sample"
MODEL = sys.argv[1]
REPEAT_NUM = int(sys.argv[2])

WORK_DIR = "evaluation"
SRC_DIR = f"benchmark"
SAVE_DIR = f"{WORK_DIR}/res/{MODEL}/{SETTING}"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

Responser = {'gpt-4': GPT4Responser, 'gpt-35-turbo': TurboResponser}[MODEL]


def load_bug_data():
    """ load data with different languages and bug types """
    res = {
        'cpp': {},
        'java': {},
        'python3': {},
    }
    files = os.listdir(SRC_DIR)
    for file in files:
        file_name = os.path.splitext(file)[0]
        lang = file_name[:file_name.find('_')]
        bug_type = file_name[file_name.find('_') + 1:]
        if bug_type in ('operation error', 'conditional statement error', 'other error', 'variable value error'):
            res[lang][bug_type] = json.load(open(os.path.join(SRC_DIR, file)))
    return res


def main():
    responser = Responser()
    debugger = IODebugger(responser)
    tester = LeetCodeTester()

    bug_data = load_bug_data()
    for i in range(1, REPEAT_NUM+1):
        for lang in bug_data.keys():
            for bug_type in bug_data[lang]:

                save_dir = os.path.join(SAVE_DIR, f"{lang}_{bug_type}_idx{i}.json")
                if not os.path.exists(save_dir):
                    bug_data_split = bug_data[lang][bug_type]
                    res = []

                    for case in tqdm.tqdm(bug_data_split, desc=f"{lang}_{bug_type}"):
                        fixed_code, fixing_exp = debugger.debug(lang=lang, code=case['buggy_code'])
                        rw, res_dict = tester.test(code=fixed_code, language=lang, task_id=case['slug'])
                        case['fixed_code'] = fixed_code
                        case['fixing_exp'] = fixing_exp
                        case['test_result_bool'] = rw
                        case['test_result_dict'] = res_dict
                        res.append(case)

                    with open(save_dir, 'w') as f:
                        json.dump(res, f, indent=4)


if __name__ == '__main__':
    main()
