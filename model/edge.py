class Edge(object):
	def __init__(self, end_point_1, end_point_2, cost, reliability):
		self.end_point_1 = end_point_1
		self.end_point_2 = end_point_2
		self.cost = cost
		self.reliability = reliability

	def __repr__(self):
		return 'endpoints: {}, cost: {}, reliability: {} \n'.format(self.end_point_1+"<->"+self.end_point_2,
                                  self.cost,
                                  self.reliability)
	def __cmp__(self, other):
		return self.getReliability().__cmp__(other.getReliability())


	def getCost(self):
		return self.cost

	def getReliability(edge):
		return edge.reliability