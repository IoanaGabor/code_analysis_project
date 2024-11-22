import tree_sitter_haskell as tshaskell
import numpy as np
from tree_sitter import Language, Parser


HS_LANGUAGE = Language(tshaskell.language())
parser = Parser(HS_LANGUAGE)

code = '''
sum' :: (Num a) => [a] -> a
sum' xs = foldl (\\acc x -> acc + x) 0 xs

'''
example_bytes = code.encode()

tree = parser.parse(example_bytes)

node = tree.root_node

def extract_features(node, parent_index=None, nodes=[], edges=[]):
    node_type = node.type  
    print("type:")
    print(node_type)
    start_pos = node.start_point  
    end_pos = node.end_point
    code_value = code[node.start_byte:node.end_byte]  
    feature_vector = [node_type, code_value, start_pos[0], start_pos[1], end_pos[0], end_pos[1]]
    node_index = len(nodes)
    nodes.append(feature_vector)

    if parent_index is not None:
        edges.append((parent_index, node_index))


    for child in node.children:
        extract_features(child, parent_index=node_index, nodes=nodes, edges=edges)

    return nodes, edges


nodes, edge_list = extract_features(node)

print(nodes)
print(edge_list)

num_nodes = len(nodes)
adj_matrix = np.zeros((num_nodes, num_nodes), dtype=np.float32)
for parent, child in edge_list:
    adj_matrix[parent, child] = 1  

print(adj_matrix)