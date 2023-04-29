import networkx as nx
import matplotlib.pyplot as plt

entity_dict = {}
with open("data/entity2id.txt", "r") as f:
    f.readline()
    for line in f:
        entity_list = line.strip().split('\t')
        entity_name, entity_id = entity_list[0], entity_list[1]
        entity_dict[int(entity_id)] = entity_name

relation_dict = {}
with open("data/relation2id.txt", "r") as f:
    f.readline()
    for line in f:
        relation_list = line.strip().split('\t')
        relation_name, relation_id = relation_list[0], relation_list[1]
        relation_dict[int(relation_id)] = relation_name

edges = []
with open("data/train2id.txt", "r") as f:
    f.readline()
    for line in f:
        edge_list = line.strip().split('\t')
        head_id, relation_id, tail_id = edge_list[0], edge_list[1], edge_list[2]
        edges.append((int(head_id), int(tail_id), int(relation_id)))


# 生成节点和边列表
nodes = set()
for edge in edges:
    nodes.add(edge[0])
    nodes.add(edge[2])
nodes = list(nodes)
edges = [(entity_dict[edge[0]], entity_dict[edge[2]], relation_dict[edge[1]]) for edge in edges]

# 使用networkx库绘制图形网络

G = nx.DiGraph()
G.add_nodes_from(nodes)
for edge in edges:
    source_node, target_node, relation = edge
#     G.add_edges_from(source_node,target_node)
    G.add_edges_from([(source_node, target_node, {'relation': relation}) for source_node, target_node, relation in edges])

# nx.draw(G, with_labels=True)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)
plt.show()
