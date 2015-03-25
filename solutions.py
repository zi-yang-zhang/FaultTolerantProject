__author__ = 'yearfun'
import reliability_calculator

def sol(mst_list, notused_list, rgoal, budget):

    notused_list = sorted(notused_list, key=lambda edge: edge.reliability, reverse=True)
    mst_list = sorted(mst_list, key=lambda edge: edge.vertice_1, reverse=True)





    info_mst,cmst,rmst = reliability_calculator.reliabilityTable (mst_list)
    print "================================================================================================="
    print 'a)   Meet  a  given  reliability  goal by calculating the reliability for fully connected network '
    allConnected_list = list(mst_list + notused_list)
    info,cost,rmax = reliability_calculator.reliabilityTable (allConnected_list)
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
        infob, costb,rb = reliability_calculator.reliabilityTable (useful_listb)
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
                infob, costb,rb = reliability_calculator.reliabilityTable (useful_listb)

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
                        infob, costb, rb  = reliability_calculator.reliabilityTable (try_listb2)
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
            infoc, costc, rc = reliability_calculator.reliabilityTable (try_listc)
            print 'Network design'
            print infoc
            print 'Network Reliability'
            print rc
            print 'Network Cost'
            print costc
    print "================================================================================================="





# simple function for calculating the cost of the list of edges
def costOfEdges(list):
    cost = 0
    for edge in list:
        cost = cost+edge.cost
    return cost