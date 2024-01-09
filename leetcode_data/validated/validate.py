import os
import json
import random
import tqdm
from leetcode_oj import LeetCodeTester

WORK_DIR = "leetcode_data/filtered"
SRC_DIR = "leetcode_data/parsed"
TESTER = LeetCodeTester()


def is_valid(solution: dict) -> bool:
    """ test whether the solution can pass leetcode OJ """

    task_id = solution['slug']
    language = solution['tags']
    code = solution['code']
    try:
        reward, result_dict = TESTER.test(code=code, task_id=task_id, language=language)
    except Exception as e:
        print(e.reason)
        reward = False

    return reward


def leetcode_validate(diverse_solutions: dict, instance_per_language: int) -> list:
    """ filter for solutions that can pass leetcode OJ """

    res = []
    for language_tag, solutions in diverse_solutions.items():
        sampled_solutions = random.sample(solutions, instance_per_language)
        for solution in tqdm.tqdm(sampled_solutions, desc=f"testing {language_tag} solutions"):
            if is_valid(solution):
                res.append(solution)
    return res


def match_qa_pairs(questions: list, solutions: list) -> tuple[list, list]:
    """ Filter questions and solutions by slugs. Only those with the same slugs will be matched. """

    question_slugs = set([question['slug'] for question in questions])
    solution_slugs = set([solution['slug'] for solution in solutions])

    mutual_slugs = question_slugs.intersection(solution_slugs)

    matched_questions = [question for question in questions if question['slug'] in mutual_slugs]
    matched_solutions = [solution for solution in solutions if solution['slug'] in mutual_slugs]

    return matched_questions, matched_solutions


def classify_solutions(matched_solutions: list) -> dict:
    """ classify solutions by language tag """

    # available_tags = {'python3', 'java', 'cpp'}
    # available_tags = {'java'}
    # available_tags = {'python3'}
    available_tags = {'cpp'}
    res = {language_tag: [] for language_tag in available_tags}

    for solution in matched_solutions:

        # make sure the language tag appears once and only once
        solution_tag = solution['tags']
        language_tag = set(solution_tag).intersection(available_tags)
        if len(language_tag) == 1:
            tag = language_tag.pop()
            solution['tags'] = tag

            # filter out the noise in the code
            original_code = solution['code'].replace("\\n", "\n").replace("\\t", "\t").replace("\\'", "\'").replace(
                '\\"', '\"').strip()
            solution['code'] = original_code

            res[tag].append(solution)

    return res


def main():
    with open(os.path.join(SRC_DIR, "questions.json")) as f:
        print("Loading questions...")
        questions = json.load(f)

    with open(os.path.join(SRC_DIR, "solutions_en.json")) as f:
        print("Loading english solutions...")
        solutions_en = json.load(f)

    diverse_solutions = classify_solutions(solutions_en)

    validated_solutions = leetcode_validate(diverse_solutions, 400)  # max to be 1000
    matched_questions, matched_solutions = match_qa_pairs(questions=questions, solutions=validated_solutions)

    with open(os.path.join(WORK_DIR, "questions.json"), "w") as f:
        json.dump(matched_questions, f, indent=4)
    with open(os.path.join(WORK_DIR, "solutions.json"), "w") as f:
        json.dump(matched_solutions, f, indent=4)


if __name__ == "__main__":
    main()
