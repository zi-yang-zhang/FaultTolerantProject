__author__ = 'yearfun'

def sol(mst_list, notused_list, rgoal, budget):

    notused_list = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    mst_list = sorted(mst_list, key=lambda edge: edge.vertice_1, reverse=True)





    info_mst,cmst,rmst = reliabilityTable (mst_list)
    print "================================================================================================="
    print 'a)   Meet  a  given  reliability  goal by calculating the reliability for fully connected network '
    allConnected_list = list(mst_list + notused_list)
    info,cost,rmax = reliabilityTable (allConnected_list)
    if rmax < rgoal:
        print 'cannot meet a given reliability goal since reliability for fully connected network is still smaller than the goal'
    else:
        print 'Network design'
        print info
        print 'Network Reliability'
        print rmax
        print 'Network Cost'
        print cost
    print "================================================================================================="
    print 'b)   Meet  a  given  reliability  goal  subject  to  a  given  cost  constraint  '
    useful_listb = list(mst_list)
    useless_listb = sorted(notused_list, key=lambda edge: edge.cost, reverse=True)
    method2 = False
    costb = -1
    if cmst > budget:
        print 'only a) can be found'
    else:
        infob, costb,rb = reliabilityTable (useful_listb)
        if rb>= rgoal:
            print 'minimum spanning tree meets reliability goal and the constrain'
            print 'Network design'
            print infob
            print 'Network Reliability'
            print rb
            print 'Network Cost'
            print costb

        else:
            last_info, last_cost, last_r = infob, costb,rb
            # sort the not-used edges by the decreasing order of cost
            # pop the least cost edge into mst
            while rb < rgoal and costb<budget and len(useless_listb) > 0:
                useful_listb.append(useless_listb.pop())
                last_info, last_cost, last_r = infob, costb, rb
                infob, costb,rb = reliabilityTable (useful_listb)

            if costb>budget: # for correcting the value, since it might jump out of while loop by cost larger than budget
                infob, costb, rb = last_info, last_cost, last_r
            if (rb<rgoal):
                method2 = True; # using method 2 if method 1 fail, method2 tend to calculate Rmax for given cost, therefore, it's not prefered
            else:
                print 'Network design'
                print infob
                print 'Network Reliability'
                print rb
                print 'Network Cost'
                print costb

            if method2:
                print'using method 2'
                useful_listb2 = list(mst_list)
                # sort the not-used edges in the decreasing order of reliability
                useless_listb2 = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
                room = budget - costOfEdges(useful_listb2)
                print 'After building the minimum spanning tree we still have $' + str(room)
                # determine if the cost of minimum spanning tree is too much or not
                if costOfEdges(mst_list) > budget:
                    print 'only a) can be found'
                else:
                    # get rid of those very expensive edges
                    for edge in useless_listb2:
                        if edge.cost> room:
                           useless_listb2.remove(edge)

                    # get rid of some expensive edges, to make sure the cost of mst and the cost of not-used edges list is under constrain
                    while costOfEdges(useless_listb2) > room:
                        useless_listb2.pop()
                    # check if cheap edges exist
                    if len(useless_listb2)==0:
                        print 'All the not used edges are too expensive to add into the network'
                    else:
                        # combine minimum spanning tree with cheap edges who has large reliability
                        try_listb2 = list(useful_listb2 + useless_listb2)
                        infob, costb, rb  = reliabilityTable (try_listb2)
                        print 'Network design'
                        print infob
                        print 'Network Reliability'
                        print rb
                        print 'Network Cost'
                        print costb

            # cannot meet the reliability goal if both methods didn't work
            if rb<rgoal:
                print 'Cannot meet the reliability goal because of the cost constrain'
                print 'only a) can  be found'
                print 'Network design'
                print infob
                print 'Network Reliability'
                print rb
                print 'Network Cost'
                print costb





    print "================================================================================================="
    print 'c)   Maximize  reliability  subject  to  a  given  cost  constraint'
    # maximizing the reliability based on the network found in part b
    useful_listc = list(useful_listb)
    useless_listc = sorted(useless_listb, key=lambda edge: edge.reliability, reverse=True)
    uselessLength = len(useless_listc)
    room = budget - costOfEdges(mst_list)
    if costb>0:
        roomb = budget - costb
    # calculate for how much more that we can spend on extra edges for redundancy
    print 'After building the minimum spanning tree we still have $' + str(room)

    if rb<rgoal:
        print 'only a) can be found'
    elif cmst == budget and rmst >= rgoal:
        print 'minimum spanning tree meets reliability goal and the constrain'
        print 'Network design'
        print info_mst
        print 'Network Reliability'
        print rmst
        print 'Network Cost'
        print cmst
    elif costb == budget and rb >=rgoal:
        # it is possible that the network found in part b is already optimal
        print 'After building the network for b) we still have $' + str(roomb)
        print 'the solution is the same as b)'
        print useless_listc
        print 'Network design'
        print infob
        print 'Network Reliability'
        print rb
        print 'Network Cost'
        print costb
    else:
        print 'After building the network for b) we still have $' + str(roomb)
        # get rid of extremely expensive edges
        for edge in useless_listc:
            if edge.cost> roomb:
                useless_listc.remove(edge)

        # remove some edges with low reliability to keep the cost with in the budget
        while costOfEdges(useless_listc) > roomb:
            useless_listc.pop()

        if len(useless_listc)==0:
            print 'All the not used edges are too expensive to add into the network'
            print 'only a) can be found'
        else:
            try_listc = list(useful_listc + useless_listc)
            infoc, costc, rc = reliabilityTable (try_listc)
            print 'Network design'
            print infoc
            print 'Network Reliability'
            print rc
            print 'Network Cost'
            print costc
    print "================================================================================================="









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