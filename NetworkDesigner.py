# The input file is in the format:
# Number of cities: A B C D ...(N cities)
# Cost/Reliability matrix: A-B,A-C,A-D...B-C,B-D...C-D....(N(N-1)/2)
import string

alphabet_list = list(string.ascii_uppercase)

class Edge(object):
	def __init__(self, end_point_1, end_point_2, cost, reliability):
		self.end_point_1 = end_point_1
		self.end_point_2 = end_point_2
		self.cost = cost
		self.reliability = reliability

	def __str__(self):
		return 'endpoints: ' + self.end_point_1  + self.end_point_2 + ' cost: ' + self.cost +' reliability: '+ self.reliability +'\n'

def readValueFromFile(filePath):
	input_file  = open(filePath)

	number_of_cities = input_file.readline()
	costs = input_file.readline().split(',')
	reliabilities = input_file.readline().split(',')
	return number_of_cities,costs,reliabilities


number_of_cities, costs,reliabilities = readValueFromFile("input_file")

city_list = alphabet_list[0:int(number_of_cities)]
minimum_spanning_tree_set = set()
edge_list = list()
reliability_list = list()
cost_list = list()
row = 0
col = 1
for reliability,cost in zip(reliabilities,costs):
	print row
	print col
	edge_list.append(Edge(city_list[row],city_list[col],cost,reliability))
	if(col == len(city_list)-1):
		row = row+1
		col = row+1
	else:
		col= col+1

	




print city_list
for edge in edge_list:
	print str(edge)


