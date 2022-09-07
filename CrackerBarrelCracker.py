#
#     0
#    0 0
#   0 0 0
#  0 0 0 0
# 0 0 0 0 0
#
# 0 | 1,2 | 3,4,5 | 6,7,8,9 | 10,11,12,13,14
# 0 | 00  | 000   |   0000  |     00000
#


STATE_WINNING = "W"
STATE_LOSING = "L"
STATE_UNDETERMINED = "U"


def generateTransitionRules():
    # start with array indexes
    transitions = [
        ( 0,  1,  3),
        ( 0,  2,  5),
        ( 1,  3,  6),
        ( 1,  4,  8),
        ( 2,  4,  7),
        ( 2,  5,  9),
        ( 3,  1,  0),
        ( 3,  4,  5),
        ( 3,  6, 10),
        ( 3,  7, 12),
        ( 4,  7, 11),
        ( 4,  8, 13),
        ( 5,  2,  0),
        ( 5,  4,  3),
        ( 5,  8, 12),
        ( 5,  9, 14),
        ( 6,  3,  1),
        ( 6,  7,  8),
        ( 7,  4,  2),
        ( 7,  8,  9),
        ( 8,  4,  1),
        ( 8,  7,  6),
        ( 9,  5,  2),
        ( 9,  8,  7),
        (10,  6,  3),
        (10, 11, 12),
        (11,  7,  4),
        (11, 12, 13),
        (12,  7,  3),
        (12,  8,  5),
        (12, 11, 10),
        (12, 13, 14),
        (13,  8,  4),
        (13, 12, 11),
        (14,  9,  5),
        (14, 13, 12)]
    # convert to bit masks
    return [tuple([2**idx for idx in tup]) for tup in transitions]


def checkIfRuleApplies(state, rule):
    return (state & rule[0]) != 0 and (state & rule[1]) != 0 and (state & rule[2]) == 0


def transition_unchecked(state, rule):
    # flip states (assumes bits state are 1, 1, 0, respectively. Flips to 0, 0, 1)
    return state ^ (rule[0] | rule[1] | rule[2])


def generateStates():
    return { state: [STATE_UNDETERMINED, []] for state in range(1, 2**15 - 1) }


def addTransitionsAndLabels(states, transitionRules):
    for key in states:
        # add any transitions
        for rule in transitionRules:
            if checkIfRuleApplies(key, rule):
                states[key][1].append(transition_unchecked(key, rule))

        # check if state is a power of 2 (assumes state > 0)
        # i.e. There is only 1 peg left
        if (key & (key - 1)) == 0:
            states[key][0] = STATE_WINNING

        # if a state has no transitions (and not already marked as a winning state) it is a losing state
        if len(states[key][1]) == 0 and states[key][0] != STATE_WINNING:
            states[key][0] = STATE_LOSING


def settleTransitiveClosureRecursive(states, state):
    if states[state][0] == STATE_UNDETERMINED:
        states[state][0] = STATE_LOSING
        for transition in states[state][1]:
            if settleTransitiveClosureRecursive(states, transition):
                states[state][0] = STATE_WINNING
    return states[state][0] == STATE_WINNING


def settleTransitiveClosure(states):
    for state in states:
        settleTransitiveClosureRecursive(states, state)


def display(state):
    vals = ["0" if (((2**i) & state) != 0) else "x" for i in range(15)]
    graph = """\
        {}
       {} {}
      {} {} {}
     {} {} {} {}
    {} {} {} {} {}
    """.format(*vals)
    print(graph)


def walkWinningState(states, s, path):
    if len(states[s][1]) == 0:
        for p in path:
            display(p)
            print()
        #    print("{}, ".format(bin(p)))
        #

        return

    for transition in states[s][1]:
        if states[transition][0] == STATE_WINNING:
            walkWinningState(states, transition, path + [transition])


def displayWinningStates(states):
    base = 2**15 - 1
    startingStates = [2**i ^ base for i in range(15)]  # All starting states.
    startingStates = [startingStates[4]]  # The basic starting state. Comment this out for all.
    for s in startingStates:
        print("\nStarting state: {}".format(bin(s)))
        print("Winnable? {}".format(states[s][0] == STATE_WINNING))
        if states[s][0] == STATE_WINNING:
            walkWinningState(states, s, [s])


def main():
    transitionRules = generateTransitionRules()
    states = generateStates()
    addTransitionsAndLabels(states, transitionRules)
    settleTransitiveClosure(states)
    displayWinningStates(states)


if __name__  == "__main__":
    main()
