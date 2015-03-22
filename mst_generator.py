
def generate(edge_list):
	print sorted(edge_list, key=lambda edge: edge.reliability, reverse=True)
