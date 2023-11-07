import networkx as nx

# function to promote a man
def promote(m):
    promoted_men.add(m)

# function to reactivate a man
def reactivate(m):
    reactivated_men.add(m)

# function to check if a woman is matched in the current matching
def is_matched(woman, matching):
    return any(pair[1] == woman for pair in matching)

# function to get the current tie for a man
def get_current_tie(m, men_prefs, matching, promoted_men, reactivated_men, stalled_men):
    for tie in men_prefs[m]:
        # check if the tie contains only unmatched women
        unmatched_women = [woman for woman in tie if not is_matched(woman, matching)]

        if not unmatched_women:
            # all women in this tie are matched
            continue

        # handle promotions, reactivations, and stalled men

        if m in promoted_men:
            # if the man is promoted, only consider women that are not promoted
            unmatched_women = [woman for woman in unmatched_women if woman not in promoted_men]

        if m in reactivated_men:
            # if the man is reactivated, only consider women that are not in stalled men's ties
            unmatched_women = [woman for woman in unmatched_women if woman not in get_stalled_women(matching, stalled_men)]

        # if the tie contains unmatched women, return it as the current tie
        if unmatched_women:
            return tie
        
    # return an empty list if no unmatched women are found in the tie
    return []

# function to promote woman ahead
def promote_woman_ahead(man, woman, men_prefs):
    if man in men_prefs:
        for tie in men_prefs[man]:
            if woman in tie:
                tie.remove(woman)
                tie.insert(0, woman) # promote the woman to the front of the tie
                return

# function to get the women in the ties of stalled men
def get_stalled_women(matching, stalled_men):
    stalled_women = set()
    for pair in matching:
        man, woman = pair
        if man in stalled_men:
            stalled_women.update(get_current_tie(man, men_prefs, matching, promoted_men, reactivated_men, stalled_men))
        return stalled_women

"""
Phase 1 of the McDermid algorithm.
"""
def phase1(men, women, men_prefs, women_prefs):
    # initialize data structures
    matching = []
    stalled_men = set() # set of stalled men
    exhausted_men = set() # set of exhausted men
    promoted_men = set() # set of promoted men
    reactivated_men = set() # set of reactivated men

    while True:
        eligible_man = None
        for man in men:
            if (
                man not in [pair[0] for pair in matching] and
                man not in stalled_men and
                (not man in promoted_men or man not in exhausted_men)
            ):
                eligible_man = man
                break

        if eligible_man is None:
            # no eligible men left, exit the loop
            break

        # check if the eligible man is exhausted
        if eligible_man in exhausted_men:
            # promote a man
            promoted_men.add(eligible_man) # add the man to the set of promoted men
            # set the man to be unexhausted
            exhausted_men.discard(eligible_man) # remove the man from the set of exhausted men
            # reactivate the man
            reactivated_men.add(eligible_man) # add the man to the set of reactivated men
            # set the man's current tie to be his first choice directly
            if eligible_man in men_prefs:
                current_tie = [men_prefs[eligible_man][0]] # get the first choice for the eligible man
                
        # get the curernt tie for the eligible man
        current_tie = get_current_tie(eligible_man, men_prefs, matching, promoted_men, reactivated_men, stalled_men)

        if not current_tie:
            # man is exhausted, mark him as exhausted
            exhausted_men.add(eligible_man)
        else:
            # man propose to a woman in the current tie
            woman = current_tie[0]
            if woman in [pair[1] for pair in matching]:
                # woman is matched to another man, remove the old matching
                old_man = [pair[0] for pair in matching if pair[1] == woman][0]
                matching.remove((old_man, woman))
                # mark the old man as reactivated
                reactivated_men.add(old_man)
                # remove the old man from the stalled set
                stalled_men.discard(old_man)
            # update the matching with the new proposal
            matching.append((eligible_man, woman))
    
    if not stalled_men:
        return matching # return the current matching
    else:
        # invoke phase 2
        return phase2(men, women, men_prefs, women_prefs, matching, stalled_men, exhausted_men, promoted_men, reactivated_men)

"""
Phase 2 of the McDermid algorithm.
"""
def phase2(men, women, men_prefs, women_prefs, matching, stalled_men):
    # create a bipartite graph
    G = nx.Graph()

    # add a men to one partition (U) and women to the other partition (V)
    G.add_nodes_from(men, bipartite=0)
    G.add_nodes_from(women, bipartite=1)

    # add edges based on men's preferences and current ties
    for man in stalled_men:
        current_tie = get_current_tie(man, men_prefs, matching)
        for woman in current_tie:
            G.add_edge(man, woman)
    
    # compute a maximum cardinality matching using Hopcroftt-Karp algorithm
    max_matching = nx.bipartite.maximum_matching(G)

    # separate the matched men and women
    matched_men = [man for man, woman in max_matching.items() if man in men]
    matched_women = [woman for woman, man in max_matching.items() if woman in women]

    # identify the sets E, O, and U
    E = set(matched_women)
    O = set(women) - E
    U = set(matched_men)

    # construct N' by removing pairs (m,w) where m is in O and w is in E
    N_prime = [(man, woman) for man, woman in max_matching.items() if not (man in O and woman in E)]

    if not N_prime:
        # if N' is empty, invoke Phase 3
        phase3(men, women, men_prefs, women_prefs, matching, stalled_men)
        pass
    else:
        # for each pair (m,w) in N'
        for man, woman in N_prime:
            # promote woman w ahead of man m's current tie
            promote_woman_ahead(man, woman, men_prefs)
            # add the pair (m,w) to the matching
            matching.append((man, woman))
            # set man m to be unstalled
            stalled_men.remove(man)
    
    # unstall all men in U who are unmatched in N
    for man in U:
        if man not in matched_men:
            stalled_men.remove(man)
    
    # continue with phase 1
    return phase1(men, women, men_prefs, women_prefs, matching, stalled_men)

"""
Phase 3 of the McDermid algorithm.
"""
def phase3(matching, N):
    for (man, woman) in N:
        matching.append((man, woman)) # add each pair to the matching M
    return matching # return the updated matching M

promoted_men = set() # assuming a list to keep track of promotions
reactivated_men = set() # assuming a list to keep track of reactivations

# list for men and women
men = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
women = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

men_prefs = {'1': [['10'], ['4'], ['6'], ['9'], ['8'], ['7'], ['1']], '2': [['9'], ['5'], ['10'], ['1'], ['8']], '3': [['1'], ['8'], ['6'], ['5'], ['2'], ['7'], ['10'], ['4']], '4': [['4'], ['1'], ['6'], ['7'], ['2'], ['8']], '5': [['2'], ['10'], ['7'], ['9'], ['6'], ['3'], ['5']], '6': [['3'], ['8']], '7': [['9'], ['7']], '8': [['8'], ['1'], ['7'], ['6'], ['9'], ['3'], ['4']], '9': [['4'], ['1'], ['10']], '10': [['2'], ['9'], ['4'], ['8'], ['10'], ['5'], ['1'], ['3']]}
women_prefs = {'1': [['9'], ['10'], ['3'], ['2'], ['4'], ['8'], ['1']], '2': [['5'], ['10'], ['3'], ['4']], '3': [['8'], ['10'], ['5'], ['6']], '4': [['8'], ['3'], ['9'], ['10'], ['4'], ['1']], '5': [['10'], ['3'], ['5'], ['2']], '6': [['8'], ['4'], ['1'], ['5'], ['3']], '7': [['1'], ['3'], ['4'], ['7'], ['5'], ['8']], '8': [['2'], ['10'], ['3'], ['6'], ['1'], ['8'], ['4']], '9': [['7'], ['10'], ['1'], ['5'], ['2'], ['8']], '10': [['2'], ['3'], ['10'], ['9'], ['1'], ['5']]}
# list to keep track of current matching
matching = []

# track the stalled and exhausted man
stalled_men = set()
exhausted_men = set()

# Phase 1
matching = phase1(men, women, men_prefs, women_prefs)

# Check if there are stalled men
if stalled_men:
    # Phase 2
    phase2_result = phase2(men, women, men_prefs, women_prefs, matching, stalled_men)

    if not phase2_result:
        # Phase 2 didn't yield any matches, proceed to Phase 3
        matching = phase3(matching, phase2_result)

print(matching)