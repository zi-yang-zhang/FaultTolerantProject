class Edge(object):
	def __init__(self, end_point_1, end_point_2, cost, reliability):
		self.end_point_1 = end_point_1
		self.end_point_2 = end_point_2
		self.cost = cost
		self.reliability = reliability

	def __str__(self):
		return 'endpoints: ' + self.end_point_1  + self.end_point_2 + ' cost: ' + self.cost +' reliability: '+ self.reliability +'\n'
