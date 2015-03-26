


# finding reliability for giving edges
def reliabilityTable (test_list):
    test_list = sorted(test_list,  key=lambda edge: edge.reliability, reverse=True)
    # build the truth table based on the number of given edges
    # the size of the truth table will be 2^(number of edges) * (number of edges)
    # the meaning of the truth table is to representing 1 for edges used, 0 for removing the edges from the network
    testtable = truthtable(len(test_list));

    r = 0
    rtmp = 1
    r_list = []
    allConnected_list = []
    cost = 0


    # cost of the network
    for edge in test_list:
        r_list.append(edge.reliability)
        cost = edge.cost + cost

    # check every row in the truth table and see if the network is still connected
    for row in testtable:
        oconnected = isAllConnected(row, test_list)
        allConnected_list.append(oconnected)


    # conver the truth table into reliability table
    # if the row[i] == 1, meaning the edge is used in the network so we put the reliability into the table
    # if row[i] == 0, meaning the edge is removed from the network,, so we put 1-reliability
    for row in testtable:
        for i in xrange(len(test_list)):
            if row[i] :
                row[i] = r_list[i]
            else:
                row[i] = 1- r_list[i]

    # get the product of each row from the reliability table
    rproduct_list = []
    for row in testtable:
        for i in xrange(len(test_list)):
            rtmp = rtmp*row[i]
        rproduct_list.append(rtmp)
        rtmp = 1

    reliability = 0

    # add the reliabilities up for all the possible all to all connected subnetwork
    for i in xrange(len(rproduct_list)):
        reliability = reliability+rproduct_list[i]*allConnected_list[i]

    return test_list, cost, reliability



# build the truth table
def truthtable (n):
    if n < 1:
        return [[]]
    subtable = truthtable(n-1)
    return [ row + [v] for row in subtable for v in [0,1] ]


# graph example {'A': set(['C']), 'C': set(['A', 'B', 'D']), 'B': set(['C', 'E']), 'E': set(['B']), 'D': set(['C'])}

# using depth first to search for the network
def dfs(graph_in, start):
    visited = set()
    stack = [start]
    graph = graph_in.copy()
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            # print vertex
            visited.add(vertex)
            stack.extend(graph[vertex] - visited)


    return visited


# check if the subnetwork is still all to all connected
# truth_list is a row from the truth table
# input_list is the list of edges
def isAllConnected(truth_list, input_list):
    cities_list = list()
    connected_cities = list()
    test_list = list(input_list)

    # need to know how many cities in the network
    for edge in test_list:
        cities_list.append(edge.vertice_1)
        cities_list.append(edge.vertice_2)

    cities_list = set(cities_list)
    cities_list = list(cities_list)
    if len(cities_list) == 0:
        return False

    # removed the edge if it is 0 in the truth table
    i = 0
    for edge in test_list:
        if truth_list[i] == 0:
            test_list.remove(edge)
        i = i+1
    for edge in test_list:
        connected_cities.append(edge.vertice_1)
        connected_cities.append(edge.vertice_2)

    # if the edges is less than the cities number -1
    # some of the cities is isolated
    if len(test_list) >= (len(cities_list)-1):
        test_graph = getGraph(test_list)
    else:
        return 0

    # check which cities will be visited
    visited_list = dfs(test_graph,connected_cities[1])
    # if the visited cities is less than the cities in the network
    # it means some cities are isolated
    if len(cities_list) > len(visited_list):
        return False

    return True

# build the graph of the network
# the edges are all bi-directional
def getGraph(test_list):
    dict_graph = {}
    for edge in test_list:
        # adding vertex into the dictionary and updating the other end of the edge into the key
        if edge.vertice_1 not in dict_graph:
            dict_graph[edge.vertice_1] = set(edge.vertice_2)
        else:
            dict_graph[edge.vertice_1].update(set(edge.vertice_2))
        if edge.vertice_2 not in dict_graph:
            dict_graph[edge.vertice_2] = set(edge.vertice_1)
        else:
            dict_graph[edge.vertice_2].update(set(edge.vertice_1))
    for key in dict_graph:
        dict_graph[key] = set(dict_graph[key])

    # print dict_graph
    return dict_graph

# simple function for calculating the cost of the list of edges
def costOfEdges(list):
    cost = 0
    for edge in list:
        cost = cost+edge.cost
    return cost