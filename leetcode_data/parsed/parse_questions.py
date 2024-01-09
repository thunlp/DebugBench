import os
import json
from bs4 import BeautifulSoup

SAVE_DIR = "leetcode_data/parsed"
SRC_DIR = "leetcode_data/scraped"
FILE_NAME = "question_all.json"


def parse_a_question(raw_question: dict) -> dict:
    # get_slug
    slug = raw_question["title_slug"]

    # get text
    html_text = raw_question['english_content']['data']['question']['content']
    soup = BeautifulSoup(html_text, 'html.parser')
    plain_text = soup.get_text()

    # remove follow up
    if "Follow up:" in plain_text:
        plain_text = plain_text[:plain_text.find("Follow up:")].strip()

    # get description:
    description = plain_text[:plain_text.find("Example 1")].strip()

    # count example number
    ex_num = 0
    while f'Example {ex_num + 1}:' in plain_text:
        ex_num += 1

    # check out constraints
    have_constraints = "Constraints:" in plain_text
    if have_constraints:
        constraints = plain_text[plain_text.find("Constraints:") + len("Constraints:"):].strip()
    else:
        constraints = ""

    # get examples
    end_idx = ex_num
    examples = []
    for ex_idx in range(1, ex_num + 1):

        head_sign = plain_text.find(f'Example {ex_idx}:') + len(f'Example {ex_idx}:')
        if ex_idx != end_idx:
            end_sign = plain_text.find(f'Example {ex_idx + 1}:')
        else:
            if have_constraints:
                end_sign = plain_text.find("Constraints:")
            else:
                end_sign = -1

        example = plain_text[head_sign: end_sign]
        examples.append(example.strip())

    res = {
        "slug": slug,
        "description": description,
        "examples": examples,
        "constraints": constraints,
    }

    return res


def parse_questions(raw_questions: list[dict]) -> list[dict]:
    res = []
    for question in raw_questions:
        res.append(parse_a_question(question))
    return res


def main():
    raw_questions = json.load(open(os.path.join(SRC_DIR, FILE_NAME)))

    parsed_questions = parse_questions(raw_questions)

    with open(os.path.join(SAVE_DIR, "questions_test.json"), "w") as f:
        json.dump(parsed_questions, f, indent=4)


if __name__ == "__main__":
    main()
