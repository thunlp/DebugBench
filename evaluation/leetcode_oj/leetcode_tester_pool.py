from leetcode_tester import LeetCodeTester
import dotenv
import os
import time

class LeetCodeTesterPool:
    def __init__(self, leetcode_sessions, csrf_tokens, cooldown=10):
        self.testers = [LeetCodeTester(leetcode_session, csrf_token, cooldown=cooldown) for leetcode_session, csrf_token in zip(leetcode_sessions, csrf_tokens)]
        self.current_tester_index = 0

    def test(self, code: str, task_id: str, language: str) -> tuple[bool, dict]:
        tester = self.testers[self.current_tester_index]
        try:
            return tester.test(code, task_id, language)
        except Exception as e:
            print(f"Tester {self.current_tester_index} failed with error: {e}")
            time.sleep(10)
            self.current_tester_index = (self.current_tester_index + 1) % len(self.testers)
            return self.test(code, task_id, language)  # Recursively try the next tester

if __name__ == '__main__':
    
    TEST_CASE = {"task_id": "make-number-of-distinct-characters-equal",
             "description": "You are given two 0-indexed strings word1 and word2.\nA move consists of choosing two indices i and j such that 0 <= i < word1.length and 0 <= j < word2.length and swapping word1[i] with word2[j].\nReturn True if it is possible to get the number of distinct characters in word1 and word2 to be equal with exactly one move. Return False otherwise.",
             "example": [{"input": "word1 = \"ac\", word2 = \"b\"", "output": "False",
                          "explanations": "Any pair of swaps would yield two distinct characters in the first string, and one in the second string."},
                         {"input": "word1 = \"abcc\", word2 = \"aab\"", "output": "True",
                          "explanations": "We swap index 2 of the first string with index 0 of the second string. The resulting strings are word1 = \"abac\" and word2 = \"cab\", which both have 3 distinct characters."},
                         {"input": "word1 = \"abcde\", word2 = \"fghij\"", "output": "True",
                          "explanations": "Both resulting strings will have 5 distinct characters, regardless of which indices we swap."}],
             "signature": "class Solution:\n    def isItPossible(self, word1: str, word2: str) -> bool:",
             "original_code": "from collections import defaultdict\nimport string\nfrom collections import Counter\nclass Solution:\n    \n    def insertAndRemove(self, mp, toInsert, toRemove): \n        mp[toInsert]+=1\n        mp[toRemove]-=1\n        \n        if(mp[toRemove]==0):\n            del mp[toRemove]     # if freq of that char reaches zero, then remove the key from dict\n        \n        \n    def isItPossible(self, word1: str, word2: str) -> bool:\n        \n        mp1, mp2 = Counter(word1), Counter(word2)  # Get freq of chars using Counter\n\t\n        \"\"\"\n        # If you are not familiar with Counters, you can simply do this:\n        mp1=defaultdict(int)\n        mp2=defaultdict(int)\n\n        for w1 in word1:\n            mp1[w1]+=1;   #store freq of chars in word1 in mp1\n\n        for w2 in word2:\n            mp2[w2]+=1;  #store freq of chars in word2 in mp2\n        \"\"\"\n\t\t\n        for c1 in string.ascii_lowercase:         # this for loop iterates through c1='a' to c1='z'\n            for c2 in string.ascii_lowercase:     # this for loop iterates through c2='a' to c2='z'\n                \n                if c1 not in mp1 or c2 not in mp2:  # if any of the char is not present then skip\n                    continue\n\n                self.insertAndRemove(mp1, c2, c1); # insert c2 to word1 and remove c1 from word1\n                self.insertAndRemove(mp2, c1, c2); # insert c1 to word2 and remove c2 from word2\n                \n                if len(mp1)== len(mp2):  # if size of both dicts are equal then possible return True\n                    return True\n\t\t\t\t\n                # reset back the maps\n                self.insertAndRemove(mp1, c1, c2); # insert c1 back to word1 and remove c2 from word1         \n                self.insertAndRemove(mp2, c2, c1); # insert c2 back to word2 and remove c1 from word2                \n        return False",
             "problematic_code": "class Solution:\n\n    def insertAndRemove(self, mp, toInsert, toRemove):\n        mp[toInsert] += 1\n        mp[toRemove] -= 1\n\n        if(mp[toRemove] == 0):\n            del mp[toRemove]\n\n    def isItPossible(self, word1: str, word2: str) -> bool:\n\n        mp1, mp2 = Counter(word1), Counter(word2)\n\n        for c1 in string.ascii_lowercase:\n            for c2 in string.ascii_lowercase:\n\n                self.insertAndRemove(mp1, c2, c1);\n                self.insertAndRemove(mp2, c1, c2);\n\n                if len(mp1) == len(mp2):\n                    return True\n\n                self.insertAndRemove(mp1, c1, c2);\n                self.insertAndRemove(mp2, c2, c1);\n        return False",
             "error_message": "Traceback (most recent call last):\n  File \"LeetCodeBug/bug_generation/src/tmp.py\", line 26, in <module>\n    assert Solution().isItPossible(word1 = \"ac\", word2 = \"b\") == False\n  File \"LeetCodeBug/bug_generation/src/tmp.py\", line 12, in isItPossible\n    mp1, mp2 = Counter(word1), Counter(word2)\nNameError: name 'Counter' is not defined\n",
             "level": "medium"}
    
    dotenv.load_dotenv()
    
    leetcode_sessions = [os.getenv(f'YOUR_LEETCODE_SESSION{i}') for i in range(1, 2)]
    csrf_tokens = [os.getenv(f'YOUR_CSRF_TOKEN{i}') for i in range(1, 2)]
    
    pools = LeetCodeTesterPool(leetcode_sessions=leetcode_sessions, csrf_tokens=csrf_tokens)

    task_id = TEST_CASE['task_id']
    code0 = TEST_CASE['original_code']
    code1 = TEST_CASE['problematic_code']
    codes = [code0, code1]

    for code in codes:
        print(pools.test(code, task_id, "python"))
    