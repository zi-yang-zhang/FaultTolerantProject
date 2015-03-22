# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)

import edge_generator


edge_list = edge_generator.generate()
	

for edge in edge_list:
	print str(edge)


