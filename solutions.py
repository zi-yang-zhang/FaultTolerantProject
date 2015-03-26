import reliability_calculator

def sol(mst_list, notused_list, rgoal, budget):

    notused_list = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    mst_list = sorted(mst_list, key=lambda edge: edge.vertice_1, reverse=True)





    info_mst,cmst,rmst = reliability_calculator.reliabilityTable (mst_list)
    print "================================================================================================="
    print 'a)   Meet  a  given  reliability  goal by adding the largest reliability edge into the the network each time '
    info,cost,rmax = findRmax(mst_list, notused_list, rgoal)
    if rmax < rgoal:
        print 'Cannot meet a given reliability goal since reliability for fully connected network is still smaller than the goal'
        print 'The fully connected network reliability is: ' + str(rmax)
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
    rb = 0
    if cmst > budget:
        if rmax < rgoal:
            print 'The network of reliability ' + str(rgoal) + 'cannot be found'
        else:
            print 'Only a) can be found'
    else:
        infob, costb,rb = reliability_calculator.reliabilityTable (useful_listb)
        if rb>= rgoal:
            print 'Minimum spanning tree meets reliability goal and the constrain'
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
                infob, costb,rb = reliability_calculator.reliabilityTable (useful_listb)

            if costb>budget: # for correcting the value, since it might jump out of while loop by cost larger than budget
                infob, costb, rb = last_info, last_cost, last_r
            if (rb<rgoal):
                method2 = True; # using method 2 if method 1 fail, method2 tend to calculate Rmax for given cost, therefore, it's not prefered


            if method2:
                useful_listb2 = list(mst_list)
                # sort the not-used edges in the decreasing order of reliability
                useless_listb2 = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
                room = budget - costOfEdges(useful_listb2)
                print 'After building the minimum spanning tree we still have $' + str(room)
                # determine if the cost of minimum spanning tree is too much or not
                if costOfEdges(mst_list) > budget:
                    print 'Only a) can be found'
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
                        infob, costb, rb  = reliability_calculator.reliabilityTable (try_listb2)


            # cannot meet the reliability goal if both methods didn't work
            if rb<rgoal:
                if rmax < rgoal:
                    print 'The network of reliability: ' + str(rgoal) + ' cannot be found'
                else:
                    print 'Only a) can  be found'
            else:
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
    useful_listc2 = list(mst_list)
    useless_listc2 = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    uselessLength = len(useless_listc)
    room = budget - costOfEdges(mst_list)
    if costb>0:
        roomb = budget - costb
    # calculate for how much more that we can spend on extra edges for redundancy
    print 'After building the minimum spanning tree we still have $' + str(room)

    if rb<rgoal:
        if rmax < rgoal:
            print 'The network of reliability: ' + str(rgoal) + ' cannot be found'
        else:
            print 'Only a) can  be found!'

    elif cmst == budget and rmst >= rgoal:
        print 'Minimum spanning tree is the optimal answer'
        print 'Network design'
        print info_mst
        print 'Network Reliability'
        print rmst
        print 'Network Cost'
        print cmst
    else:

        # c1 is building the network on top of the network of solution b)
        # c2 is building the network on top of the minimum spanning tree
        infoc1, costc1, rc1 = findRc(useful_listc, useless_listc, roomb)
        infoc2, costc2, rc2 = findRc(useful_listc2, useless_listc2, room)

        # if the edge left are too expensive to be added into the network,
        # the optimal reliability of it should be the same as in b)
        if rc1==0:
            infoc1, costc1, rc1 = infob, costb, rb


        if rc1 > rc2:
            print 'After building the network for b) we still have $' + str(roomb)
            print 'Network design'
            print infoc1
            print 'Network Reliability'
            print rc1
            print 'Network Cost'
            print costc1
        else:
            print 'Network design'
            print infoc2
            print 'Network Reliability'
            print rc2
            print 'Network Cost'
            print costc2
    print "================================================================================================="





# simple function for calculating the cost of the list of edges
def costOfEdges(list):
    cost = 0
    for edge in list:
        cost = cost+edge.cost
    return cost


def findRc(useful_list, useless_list, room):
    info, cost, rmax = [], 0, 0
    for edge in useless_list:
        if edge.cost> room:
            useless_list.remove(edge)

        # remove some edges with low reliability to keep the cost with in the budget
    while costOfEdges(useless_list) > room:
        useless_list.pop()

    if len(useless_list)>0:
        try_listc = list(useful_list + useless_list)
        info, cost, rmax = reliability_calculator.reliabilityTable (try_listc)
    return info, cost, rmax

# for finding the solution for a)
def findRmax(useful_list, useless_list, rgoal):
    useless_list = sorted(useless_list,key=lambda edge: edge.reliability, reverse=False)
    try_list = list(useful_list)
    info, cost, rmax = reliability_calculator.reliabilityTable (try_list)

    # increment the edge having the largest reliability into the network each time and compare to the rgoal
    while (rgoal>rmax) and len(useless_list)>0:
        try_list.append(useless_list.pop())
        info, cost, rmax = reliability_calculator.reliabilityTable (try_list)

    return info, cost, rmax