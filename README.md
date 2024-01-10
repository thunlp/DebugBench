# Repo of DebugBench

<img src="figs/icon.png" style="width: 20vw; height: auto;" alt="icon"> 

### Overview

Implementation for paper DebugBench: Evaluating Debugging Capabilities of Large Language Models with datasets, prompts, model outputs.



### Benchmark

Please refer to the [Hugging Face Dataset](https://huggingface.co/datasets/Rtian/DebugBench) for the data source and evaluation script if you want to use the benchmark.

DebugBench is a Large Language Model (LLM) debugging benchmark introduced in the paper "DebugBench: Evaluating Debugging Capability of Large Language Models" [url]. We collect code snippets from the [LeetCode](https://leetcode.com/) community and implant bugs into source data with [GPT-4](https://openai.com/research/gpt-4). 

- It consists of 4,253 instances.
- It covers four major bug categories and 18 minor types.
- It includes C++, Java, and Python instances.
- It contains three difficulty levels: easy, medium, and hard.
- All the instances were released after June 2022.
- Please refer to the article [url] for more details.



### Repo Content

This repository contains the implementation for benchmark construction and evaluation.

- `benchmark` directory contains the 51 JSON shards of different languages and bug types of the benchmark. 
- `dataset_construction` directory contains the implementation for bug implantation to solution code via LLMs.

- `evaluation` directory contains the implementation for evaluating the debugging capabilities of LLMs with API. 
- `evalution_result` directory contains the model output of `gpt-4-0613` ,  `gpt-3.5-turbo-0613`  and `CodeLlama-34b-instruct` under different scenarios. 

More elements will be added to the repository soon.



### Citations

Please cite the paper and star the repo if you use DebugBench and find it helpful.

Feel free to contact trc20@mails.tsinghua.edu.cn or open an issue if you have any questions.

```latex
---
license: apache-2.0
task_categories:
- text-generation
- question-answering
- conversational
language:
- en
tags:
- code
pretty_name: DebugBench
size_categories:
- 1K<n<10K


---

<img src="fig/icon.png" alt="icon" style="zoom:20%;" /> 

#### Dataset Summary

DebugBench is a Large Language Model (LLM) debugging benchmark introduced in the paper "DebugBench: Evaluating Debugging Capability of Large Language Models" [url]. We collect code snippets from the [LeetCode](https://leetcode.com) community and implant bugs into source data with [GPT-4](https://openai.com/research/gpt-4). The project is also open-sourced as a [GitHub repository](https://github.com/thunlp/DebugBench).<br>

- It consists of 4,253 instances.
- It covers four major bug categories and 18 minor types.
- It includes C++, Java, and Python instances.
- It contains three difficulty levels: easy, medium, and hard.
- All the instances were released after June 2022.
- Please refer to the article [url] for more details.



#### Data Fields

An instance in DebugBench contains 13 features.

|       Feature        | Description                                                  | Example                                                      |
| :------------------: | ------------------------------------------------------------ | ------------------------------------------------------------ |
|         slug         | The id of the leetcode programming problem.                  | single-number                                                |
|       Category       | The category of bug taxonomy.                                | logic error                                                  |
|       subtype        | The subtype of bug taxonomy under the big category.          | operation error                                              |
|       language       | The programming language of the instance.                    | cpp                                                          |
|        level         | The level of complexity of the problem from "easy", to "medium" and "hard". | easy                                                         |
|     release_time     | Release time of corresponding programming problem in the format of Unix timestamp. | 1,691,549,090                                                |
|       question       | The text description for the programming problem.            | Given a non-empty array of integers nums, every element appears twice except for one. Find that single one. You must implement a solution with a linear runtime complexity and use only constant extra space. |
|       examples       | Some examples of input-output pairs for the targeted function. | [ "Input: nums = [2,2,1]\nOutput: 1", "Input: nums = [4,1,2,1,2]\nOutput: 4", "Input: nums = [1]\nOutput: 1" ] |
|     constraints      | The constraints of input parameters.                         | 1 <= nums.length <= 3 * 104 -3 * 104 <= nums[i] <= 3 * 104 Each element in the array appears twice except for one element which appears only once. |
|       solution       | Ground-truth solutions that pass all the test suites for the programming problems. | class Solution { public: int singleNumber(vector<int>& nums) { unordered_map<int,int> mp; for(int i=0;i<nums.size();i++){ mp[nums[i]]++; } for(auto m:mp){ if(m.second==1){ return m.first; } } return -1; } }; |
| solution explanation | The original posts that share the solution.                  | \# Using Map\n```\nclass Solution {\npublic:\n int singleNumber(vector<int>& nums) {\n unordered_map<int,int> mp;\n for(int i=0;i<nums.size();i++){\n mp[nums[i]]++;\n }\n for(auto m:mp){\n if(m.second==1){\n return m.first;\n }\n }\n return -1;\n }\n};\n```\n# Using XOR\n```\nclass Solution {\npublic:\n int singleNumber(vector<int>& nums) {\n int res=0;\n for(int i=0;i<nums.size();i++){\n res^=nums[i];\n }\n return res;\n }\n};\n``` |
|      buggy_code      | The buggy version of the solution waiting to be debugged.    | class Solution { public: int singleNumber(vector<int>& nums) { unordered_map<int,int> mp; for(int i=0;i<nums.size();i++){ mp[nums[i]] = 1; } for(auto m:mp){ if(m.second==1){ return m.first; } } return -1; } }; |
|   bug_explanation    | Explanation about the implanted bug.                         | Instead of incrementing the map's value, we are setting it to 1 each time. |



#### Data Splits

The dataset is an evaluation benchmark and there comprises only one split, the eval split of 4, 253.



#### Evaluation

The evaluation is based on the unseen test suites from [LeetCode](https://leetcode.com), a popular programming challenge platform. The evaluator will need a leetcode account for the usage of test suites. To obtain the 'leetcode_session' cookie, they may utilize the developer view in their web browsers like [Chrome](https://www.google.com/chrome/) or use browser extensions like [EditThisCookie](https://chromewebstore.google.com/detail/fngmhnnpilhplaeedifhccceomclgfbg).

Please refer to the following code example for evaluation. This example is accessible in this Hugging Face repository. The leetcode_env package comes from [Leetcode Hard Gym](https://github.com/GammaTauAI/leetcode-hard-gym). More implementation details are available in [our GitHub repository](https://github.com/thunlp/DebugBench).

```python
import os
from .leetcode_env.environment import LeetCodeEnv
from .leetcode_env.types import LeetCodeSubmission, ProgrammingLanguage

LEETCODE_SESSION_COOKIE = os.environ['LEETCODE_SESSION']
class LeetCodeTester(object):

    def __init__(self):
        os.environ['LEETCODE_SESSION'] = LEETCODE_SESSION_COOKIE
        self.env = LeetCodeEnv(cooldown=15)
        self.lang_dict = {
            "python3": ProgrammingLanguage.PYTHON3,
            "java": ProgrammingLanguage.JAVA,
            "cpp": ProgrammingLanguage.CPP,
        }

    def test(self, code: str, task_id: str, language: str) -> tuple[bool, dict]:
        lang = self.lang_dict.get(language)
        sub = LeetCodeSubmission(code=code, lang=lang, question_slug=task_id)
        status, reward, done, submission_result = self.env.step(sub)
        return reward, submission_result
```

```python
if __name__ == '__main__':

    tester = LeetCodeTester()
    task_id = "make-number-of-distinct-characters-equal"
    code = "class Solution:\n\n    def insertAndRemove(self, mp, toInsert..."  # abbreviated
    print(tester.test(code, task_id, "python3"))
```

Here are two output examples.

```python
(True, {'status_code': 10, 'lang': 'python3', 'run_success': True, 'status_runtime': '111 ms', 'memory': 18488000, 'question_id': '2615', 'elapsed_time': 133, 'compare_result': '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', 'code_output': '', 'std_output': '', 'last_testcase': '', 'expected_output': '', 'task_finish_time': 1704769340887, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 99, 'total_testcases': 99, 'runtime_percentile': 73.75, 'status_memory': '18.5 MB', 'memory_percentile': 15.625, 'pretty_lang': 'Python3', 'submission_id': '1141026534', 'status_msg': 'Accepted', 'state': 'SUCCESS'})
(False, {'status_code': 11, 'lang': 'python3', 'run_success': True, 'status_runtime': 'N/A', 'memory': 18532000, 'question_id': '2615', 'elapsed_time': 184, 'compare_result': '101110111101010010111100110101111111011010100001111101011111000111010111000111101011011011101110011', 'code_output': 'false', 'std_output': '', 'last_testcase': '"abcc"\n"aab"', 'expected_output': 'true', 'task_finish_time': 1704769355341, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 64, 'total_testcases': 99, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python3', 'submission_id': '1141026664', 'input_formatted': '"abcc", "aab"', 'input': '"abcc"\n"aab"', 'status_msg': 'Wrong Answer', 'state': 'SUCCESS'})

```



#### Dataset Creation

![construct](fig/construct.png)

As illustrated in the figure above, to construct DebugBench, we collect code snippets from the LeetCode community, implant bugs into source data with GPT-4, and assure quality checks. We also evaluate two commercial and three open-source models in a zero-shot scenario. Please refer to the article [url] for more details.



#### Limitation

- Bug instances in our experiments are synthetically created and might not entirely reflect the intricacies of real-world debugging scenarios.
- For a few bug subtypes, some bug instances may have an inconsistent taxonomy nature than the labeled feature. An example of this is a bug generated in response to a prompt specifying 'undefined methods.' Rather than invoking undefined functions as expected, the code triggers an infinite loop.



#### Citation Information

```latex
@misc{tian2024debugbench,
      title={DebugBench: Evaluating Debugging Capability of Large Language Models}, 
      author={Runchu Tian and Yining Ye and Yujia Qin and Xin Cong and Yankai Lin and Zhiyuan Liu and Maosong Sun},
      year={2024},
      eprint={2401.04621},
      archivePrefix={arXiv},
      primaryClass={cs.SE}
}
```


```
