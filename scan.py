import pickle

arr = pickle.load(open("sample.pkl", "rb"))
(max, min) = (0 , 0)
(max_node, min_node) = (None, None)
for temp in arr:
	if temp is not None:
		for nodes in temp:
			for Q in nodes.Q_VALUES:
				if Q > max:
					max = Q
					max_node = nodes
				if Q < min:
					min = Q
					min_node = nodes

print(f"MAX Q_VALUE NODE")
print(f"tc: {max_node.index_list%10}")
print(f"Index: {max_node.index_act}")
print(f"{max_node.Q_VALUES}\n")
print(f"MIN Q_VALUE NODE")
print(f"tc: {min_node.index_list%10}")
print(f"Index: {min_node.index_act}")
print(f"{min_node.Q_VALUES}\n")
