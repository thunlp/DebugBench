IO_BASE_PROMPT = """

Observe the following {LANG} faulty code which is complete with no extra context. Your task is to fix up the code and explain on the modification in less than 20 words.
You have to write the fixed code again. You should put <code></code> and <exp></exp> on the boundary of the code and the explanation. Do not write anything else in your response. Your reply should be like this:
<code>
fixed code
</code>
<exp>
short explanation about the bug
</exp>
"""
IO_INTENTION_PROMPT = """Observe the function intention and its corresponding {LANG} implementation which is complete with no extra context. The implementation is faulty. Your task is to fix up the code and explain on the modification in less than 20 words.
You have to write the fixed code again. You should put <code></code> and <exp></exp> on the boundary of the code and the explanation. Do not write anything else in your response. Your reply should be like this:
<code>
fixed code
</code>
<exp>
short explanation about the bug
</exp>"""

IO_EX_PROMPT = """"""

IO_TRACEBACK_PROMPT = """Observe the following {LANG} faulty code which is complete with no extra context and its traceback messages. Your task is to fix up the code and explain on the modification in less than 20 words.
You have to write the fixed code again. You should put <code></code> and <exp></exp> on the boundary of the code and the explanation. Do not write anything else in your response. Your reply should be like this:
<code>
fixed code
</code>
<exp>
short explanation about the bug
</exp>"""

IO_COMPLETE_SYSTEM_INFO = """Observe the program question and {LANG} implementation schema. Your task is to complete the implementation. 
You should write the completed code again. You should put <code></code> on the boundary of the code. Do not write anything else in your response. Your reply should be like this:
<code>
completed code
</code>"""

IO_COMPLETE_USER_PROMPT = """- Program Question
{INTENTION}
- Implementation Schema
{SIGNATURE}
"""

EXTRACT_SIGNATURE_PROMPT = """Observe the following code. Your task extract ONLY the class & function SIGNATURE. Wrap the cleaned code with <code>, </code>. Do not write anything else in the response. Do not forget the class. Do not miss any functions.
Here are some examples.

- User Input
class Solution {
public:
    string gcdOfStrings(string str1, string str2) {

        if(str1+str2==str2+str1)
        {
            return str1.substr(0,gcd(str1.length(),str2.length()));
        }
        else{
            return "";
        }
        
    }
};
- Response
<code>class Solution {
public:
    string gcdOfStrings(string str1, string str2);
};</code>

- User Input
class Solution {
    public Node connect(Node node) {
        Map<Integer, List<Node>> map = new HashMap<>();
        goDFS(0, node, map);
        for (int key : map.keySet()) {
            List<Node> list = map.get(key);
            for (int i = 1; i < list.size(); i++) {
                list.get(i - 1).next = list.get(i);
            }
        }
        return node;
    }

    private void goDFS(int lvl, Node node, Map<Integer, List<Node>> map) {
        if (node == null) return;

        List<Node> list = map.computeIfAbsent(lvl, k -> new ArrayList<>());
        list.add(node);
        lvl++;
        goDFS(lvl, node.left, map);
        goDFS(lvl, node.right, map);
    }
}
- Response
<code>class Solution {
    public Node connect(Node node);
    private void goDFS(int lvl, Node node, Map<Integer, List<Node>> map);
}</code>

- User Input
def tsum(root):
    if(root==None):
        return 0
    x= root.val+tsum(root.left)+tsum(root.right)
    return x
def fun(root,sm,mx):
    if(root==None):
        return 0
    a=fun(root.left,sm,mx)
    b=fun(root.right,sm,mx)
    mx[0]=max(mx[0],a*(sm-a),b*(sm-b))
    return a+b+root.val
    
class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:
        mx=[0]
        sm=tsum(root)
        memo={}
        fun(root,sm,mx)
        return mx[0]%(10**9+7)
- Response
<code>def tsum(root):
def fun(root,sm,mx):
class Solution:
    def maxProduct(self, root: Optional[TreeNode]) -> int:</code>
"""