from main import *

# 5 pts
def test_huffman_simple():
    """ example from class """
    f = Counter(["A", "A", "A", "A", "A", "A", "A", "A", "A", "B", "C", "D"])
    T = make_huffman_tree(f)
    C = get_code(T)
    assert huffman_cost(C, f) == 17

# 5 pts
def test_huffman_complex():
    """ example from class """
    f = Counter(["A", "A", "A", "A", "A", "A", "A", "A", "A", "B", "C", "D",
                 "E", "F", "G", "H", "I", "J"])
    T = make_huffman_tree(f)
    C = get_code(T)
    assert huffman_cost(C, f) == 47
