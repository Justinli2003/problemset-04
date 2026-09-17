import math, queue
from collections import Counter

####### Problem 1 #######

class TreeNode(object):
    # we assume data is a tuple (frequency, character)
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
    def __lt__(self, other):
        return(self.data < other.data)
    def children(self):
        return((self.left, self.right))
    
def get_frequencies(fname):
    f=open(fname, 'r')
    C = Counter()
    for l in f.readlines():
        C.update(Counter(l))
    return(dict(C.most_common()))

# given a dictionary f mapping characters to frequencies, 
# create a prefix code tree using Huffman's algorithm
def make_huffman_tree(f):
    p = queue.PriorityQueue()
    # construct heap from frequencies, the initial items should be
    # the leaves of the final tree
    for c in f.keys():
        p.put(TreeNode(None,None,(f[c], c)))

    # greedily remove the two nodes x and y with lowest frequency,
    # create a new node z with x and y as children,
    # insert z into the priority queue (using an empty character "")
    while (p.qsize() > 1):
        # the two lowest-frequency nodes currently in the queue
        x = p.get()
        y = p.get()
        # merge them under a new internal node whose frequency is the sum.
        # internal nodes carry the empty character "" since they do not
        # correspond to a symbol of the alphabet.
        z = TreeNode(x, y, (x.data[0] + y.data[0], ""))
        p.put(z)

    # return root of the tree
    return p.get()

# perform a traversal on the prefix code tree to collect all encodings
def get_code(node, prefix="", code=None):
    """
    Traverse the prefix code tree, appending '0' when we descend left and
    '1' when we descend right. When we reach a leaf (which represents a
    character of the alphabet) we store the accumulated prefix as that
    character's encoding.

    Note: `code` defaults to None rather than {} on purpose -- a mutable
    default argument is created once and shared by every call, so successive
    calls to get_code would otherwise accumulate stale encodings from
    previously built trees.
    """
    if code is None:
        code = {}
    if node is None:
        return code

    left, right = node.children()
    if left is None and right is None:
        # leaf; node.data is the tuple (frequency, character)
        # the prefix is "" only when the tree is a single node (an alphabet
        # of size 1), in which case we still need one bit to encode it.
        code[node.data[1]] = prefix if prefix != "" else "0"
        return code

    get_code(left, prefix + "0", code)
    get_code(right, prefix + "1", code)
    return code

# given an alphabet and frequencies, compute the cost of a fixed length encoding
def fixed_length_cost(f):
    """
    With an alphabet of size |S|, a fixed-length code needs ceil(lg |S|)
    bits for every character, so the total cost is that width times the
    number of characters in the document.
    """
    sigma = len(f)
    if sigma == 0:
        return 0
    bits = max(1, math.ceil(math.log2(sigma)))
    return bits * sum(f.values())

# given a Huffman encoding and character frequencies, compute cost of a Huffman encoding
def huffman_cost(C, f):
    """
    Each occurrence of character c costs len(C[c]) bits, so the total is
    the frequency-weighted sum of the code lengths.
    """
    return sum(len(C[c]) * f[c] for c in f.keys())

f = get_frequencies('f1.txt')
print("Fixed-length cost:  %d" % fixed_length_cost(f))
T = make_huffman_tree(f)
C = get_code(T)
print("Huffman cost:  %d" % huffman_cost(C, f))


