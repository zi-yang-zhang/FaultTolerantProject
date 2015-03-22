# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)

import edge_generator,mst_generator


city_list, edge_list = edge_generator.generate()
	

#for edge in edge_list:
#	print str(edge)
sorted_edge_list = sorted(edge_list, key=lambda edge: edge.reliability, reverse=True)


mst =  mst_generator.kruskal(city_list, sorted_edge_list)

reliability_mst = 1
for edge in mst:
	reliability_mst = reliability_mst*edge.reliability

edge_set = set(sorted_edge_list)
mst_set = set(mst)

unused_edge = edge_set.difference(mst_set)


print mst
print unused_edge
print reliability_mst