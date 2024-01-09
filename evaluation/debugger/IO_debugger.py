from .prompt import IO_BASE_PROMPT, IO_INTENTION_PROMPT, IO_TRACEBACK_PROMPT, IO_EX_PROMPT
from .responser import Responser, TurboResponser

TEST_CASE = {
    "slug": "sort-list",
    "description": "Given the head of a linked list, return the list after sorting it in ascending order.",
    "examples": [
        "Input: head = [4,2,1,3]\nOutput: [1,2,3,4]",
        "Input: head = [-1,5,3,4,0]\nOutput: [-1,0,3,4,5]",
        "Input: head = []\nOutput: []"
    ],
    "constrains": "The number of nodes in the list is in the range [0, 5 * 104].\n-105 <= Node.val <= 105",
    "release_time": 1692157711,
    "oracle_code": "/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode() : val(0), next(nullptr) {}\n *     ListNode(int x) : val(x), next(nullptr) {}\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* sortList(ListNode* head) {\n        vector<int>vec1;\n    ListNode*temp= head;\n    while(temp!=NULL){\nvec1.push_back(temp->val);\ntemp= temp->next;\n    }\n    sort(vec1.begin(),vec1.end());\n    ListNode*curr= head;\n   for(int i=0;i<vec1.size();i++){\n       curr->val=vec1[i];\n       curr= curr->next;\n   }\n   return head;\n    }\n    \n\n};",
    "content": "# Intuition\\n<!-- Describe your first thoughts on how to solve this problem. -->\\n\\n# Approach\\n<!-- Describe your approach to solving the problem. -->\\n\\n# Complexity\\n- Time complexity:\\n<!-- Add your time complexity here, e.g. $$O(n)$$ -->\\n\\n- Space complexity:\\n<!-- Add your space complexity here, e.g. $$O(n)$$ -->\\n\\n# Code\\n```\\n/**\\n * Definition for singly-linked list.\\n * struct ListNode {\\n *     int val;\\n *     ListNode *next;\\n *     ListNode() : val(0), next(nullptr) {}\\n *     ListNode(int x) : val(x), next(nullptr) {}\\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\\n * };\\n */\\nclass Solution {\\npublic:\\n    ListNode* sortList(ListNode* head) {\\n        vector<int>vec1;\\n    ListNode*temp= head;\\n    while(temp!=NULL){\\nvec1.push_back(temp->val);\\ntemp= temp->next;\\n    }\\n    sort(vec1.begin(),vec1.end());\\n    ListNode*curr= head;\\n   for(int i=0;i<vec1.size();i++){\\n       curr->val=vec1[i];\\n       curr= curr->next;\\n   }\\n   return head;\\n    }\\n    \\n\\n};\\n\\n```",
    "level": "medium",
    "buggy_code": "\n/**\n * Definition for singly-linked list.\n * struct ListNode {\n *     int val;\n *     ListNode *next;\n *     ListNode() : val(0), next(nullptr) {}\n *     ListNode(int x) : val(x), next(nullptr) {}\n *     ListNode(int x, ListNode *next) : val(x), next(next) {}\n * };\n */\nclass Solution {\npublic:\n    ListNode* sortList(ListNode* head) {\n        vector<int>vec1;\n    ListNode*temp= head;\n    while(temp!=NULL){\nvec1.push_back(temp->val);\ntemp= temp->next;\n    sort(vec1.begin(),vec1.end());\n    ListNode*curr= head;\n   for(int i=0;i<vec1.size();i++){\n       curr->val=vec1[i];\n       curr= curr->next;\n   }\n   return head;\n}\n",
    "explanations": "\nThe missing closing braces for the while loop results in wrong logic and compilation error.\n"
}


class IODebugger(object):

    def __init__(self, responser: Responser):
        self.responser = responser

    def debug(self, lang: str, code: str, intention=None, case=None, traceback=None):

        if intention:
            system_prompt = IO_INTENTION_PROMPT.replace("{LANG}", lang)
        elif case:
            system_prompt = IO_EX_PROMPT.replace("{LANG}", lang)
        elif traceback:
            system_prompt = IO_TRACEBACK_PROMPT.replace("{LANG}", lang)
        else:
            system_prompt = IO_BASE_PROMPT.replace("{LANG}", lang)

        if traceback:
            user_prompt = code + f'\nTraceback\n{traceback}'
        elif intention:
            user_prompt = f'\nIntention\n{intention}' + f'\nImplementation\n{code}'
        else:
            user_prompt = code

        response = self.responser.respond(system_info=system_prompt, user_prompt=user_prompt)
        code_head = response.find('<code>') + len('<code>')
        code_end = response.find('</code>')
        exp_head = response.find('<exp>') + len('<exp>')
        exp_end = response.find('</exp>')
        code = response[code_head:code_end]
        exp = response[exp_head:exp_end]

        return code, exp


if __name__ == "__main__":
    lang = "python3"
    responser = TurboResponser()
    # responser = GPT4Responser()
    debugger = IODebugger(responser)
    code, exp = debugger.debug(lang=lang, code=TEST_CASE['buggy_code'],
                               traceback="There is no traceback for this instance.")
    print(code, exp)
