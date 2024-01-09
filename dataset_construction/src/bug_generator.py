from responser import Responser, TurboResponser, GPT4Responser

BUG_PROMPT = """Observe the following {LANG} implementation. Your task is to first add a(n) {BUG_TYPE} bug to the code and then to explain the bug you add in 15 words.
You have to write the implementation again. You should put <bug> </bug>, <exp> </exp> in the beginning and end of the code and explanation. Make sure the bug incurs unexpected behaviors. Do not write anything else in your response. 
You MUST NOT ADD ANY COMMENT ABOUT THE BUG IN CODE. Your reply should be like this: 
<bug>
code with bug
</bug>
<exp>
short explanation about the bug
</exp>
"""

TEST_CASE = {
    "slug": "minimum-total-cost-to-make-arrays-unequal",
    "description": "You are given two 0-indexed integer arrays nums1 and nums2, of equal length n.\nIn one operation, you can swap the values of any two indices of nums1. The cost of this operation is the sum of the indices.\nFind the minimum total cost of performing the given operation any number of times such that nums1[i] != nums2[i] for all 0 <= i <= n - 1 after performing all the operations.\nReturn the minimum total cost such that nums1 and nums2 satisfy the above condition. In case it is not possible, return -1.",
    "examples": [
        "Input: nums1 = [1,2,3,4,5], nums2 = [1,2,3,4,5]\nOutput: 10\nExplanation: \nOne of the ways we can perform the operations is:\n- Swap values at indices 0 and 3, incurring cost = 0 + 3 = 3. Now, nums1 = [4,2,3,1,5]\n- Swap values at indices 1 and 2, incurring cost = 1 + 2 = 3. Now, nums1 = [4,3,2,1,5].\n- Swap values at indices 0 and 4, incurring cost = 0 + 4 = 4. Now, nums1 =[5,3,2,1,4].\nWe can see that for each index i, nums1[i] != nums2[i]. The cost required here is 10.\nNote that there are other ways to swap values, but it can be proven that it is not possible to obtain a cost less than 10.",
        "Input: nums1 = [2,2,2,1,3], nums2 = [1,2,2,3,3]\nOutput: 10\nExplanation: \nOne of the ways we can perform the operations is:\n- Swap values at indices 2 and 3, incurring cost = 2 + 3 = 5. Now, nums1 = [2,2,1,2,3].\n- Swap values at indices 1 and 4, incurring cost = 1 + 4 = 5. Now, nums1 = [2,3,1,2,2].\nThe total cost needed here is 10, which is the minimum possible.",
        "Input: nums1 = [1,2,2], nums2 = [1,2,2]\nOutput: -1\nExplanation: \nIt can be shown that it is not possible to satisfy the given conditions irrespective of the number of operations we perform.\nHence, we return -1."
    ],
    "constrains": "n == nums1.length == nums2.length\n1 <= n <= 105\n1 <= nums1[i], nums2[i] <= n",
    "release_time": 1670688279,
    "oracle_code": "class Solution:\n    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:\n        n=len(nums1)\n        z=Counter(nums1)\n        z1=Counter(nums2)\n        for i in z:\n            if(n-z1[i]<z[i]):\n                return -1\n            if(z[i]>=n//2+1 and z1[i]>=n//2+1):\n                return -1\n        for i in z1:\n            if(n-z[i]<z1[i]):\n                return -1\n            if(z[i]>=n//2+1 and z1[i]>=n//2+1):\n                return -1\n        z=Counter([])\n        ans=0\n        flag=0\n        d=defaultdict(list)\n        vis=[0 for i in range(n)]\n        for i in range(n):\n            if(nums1[i]==nums2[i]):\n                z[nums2[i]]+=1\n                ans+=i\n                flag=1\n                d[nums2[i]].append(i)\n        t=0\n        l=z.most_common(len(z))\n        a=0\n        for i in range(1,len(l)):\n            a+=l[i][1]\n            for j in d[l[i][0]]:\n                vis[j]=1\n            z[l[i][0]]=0\n        if(l and a>=l[0][1]):\n            return ans\n        x=0\n        if(l):\n            x=l[0][1]-a\n            z[l[0][0]]=x\n        print(z,ans)\n        for j in z:\n            if(z[j]):\n                for i in range(n):\n                    if(vis[i]==0 and nums1[i]!=j and nums2[i]!=j and x):\n                        if(flag):\n                            ans+=i\n                            x-=1\n        return ans",
    "content": "# Complexity\\n- Time complexity:\\n<!-- Add your time complexity here, e.g. $$O(n)$$ -->\\n    O(n)\\n\\n- Space complexity:\\n<!-- Add your space complexity here, e.g. $$O(n)$$ -->\\n\\n    O(n)\\n# Code\\n```\\nclass Solution:\\n    def minimumTotalCost(self, nums1: List[int], nums2: List[int]) -> int:\\n        n=len(nums1)\\n        z=Counter(nums1)\\n        z1=Counter(nums2)\\n        for i in z:\\n            if(n-z1[i]<z[i]):\\n                return -1\\n            if(z[i]>=n//2+1 and z1[i]>=n//2+1):\\n                return -1\\n        for i in z1:\\n            if(n-z[i]<z1[i]):\\n                return -1\\n            if(z[i]>=n//2+1 and z1[i]>=n//2+1):\\n                return -1\\n        z=Counter([])\\n        ans=0\\n        flag=0\\n        d=defaultdict(list)\\n        vis=[0 for i in range(n)]\\n        for i in range(n):\\n            if(nums1[i]==nums2[i]):\\n                z[nums2[i]]+=1\\n                ans+=i\\n                flag=1\\n                d[nums2[i]].append(i)\\n        t=0\\n        l=z.most_common(len(z))\\n        a=0\\n        for i in range(1,len(l)):\\n            a+=l[i][1]\\n            for j in d[l[i][0]]:\\n                vis[j]=1\\n            z[l[i][0]]=0\\n        if(l and a>=l[0][1]):\\n            return ans\\n        x=0\\n        if(l):\\n            x=l[0][1]-a\\n            z[l[0][0]]=x\\n        print(z,ans)\\n        for j in z:\\n            if(z[j]):\\n                for i in range(n):\\n                    if(vis[i]==0 and nums1[i]!=j and nums2[i]!=j and x):\\n                        if(flag):\\n                            ans+=i\\n                            x-=1\\n        return ans\\n```",
    "level": "hard"
}


class BugGenerator(object):

    def __init__(self, responser):
        self.responser = responser

    def generate_bug(self, lang: str, bug_type: str, code: str) -> tuple[str, str]:
        """
        ask gpt-4 to generate a buggy python code
        :param code: the target code
        :return: buggy code
        """
        response = self.responser.respond(system_info=BUG_PROMPT.replace('{LANG}', lang).replace('{BUG_TYPE}', bug_type), user_prompt=code)
        bug_head = response.find('<bug>') + len('<bug>')
        bug_end = response.find('</bug>')
        exp_head = response.find('<exp>') + len('<exp>')
        exp_end = response.find('</exp>')
        bug = response[bug_head:bug_end]
        exp = response[exp_head:exp_end]

        return bug, exp


if __name__ == '__main__':

    """ test """
    responser = TurboResponser()
    bug_generator = BugGenerator(responser)
    code = TEST_CASE["oracle_code"]
    bug, exp = bug_generator.generate_bug(code=code, lang="python", bug_type="syntax bugs")
    print(bug)
    print(exp)
