"""
GSA1: Gale-Shapley Algorithm 1
While there exists an active man m, he proposes to his favourite woman w. 
- If w accepts his proposal, they become engaged. 
- If w rejects him, m deletes w from his list.
When a woman gets a new proposal from man m, she always accepts this proposal if she 
is a maiden. She also accepts this new proposal if she prefers m to her current fiance. 
Otherwise she rejects m.

If w accepted m, then she rejects her previous fiance, if there was one (breaks off 
her engagement), and becomes engaged to m.
If m was engaged to a woman w and later w rejects him, then m becomes active again, 
and deletes w from his list.

If the list m becomes empty for the first time, he turns into a bachelor, 
his original list is recovered, and he reactivates himself.

If the list of m becomes empty for the second time, he will turn into an 
old bachelor and will remain inactive forever.
"""

def gsa1(men_preferences, women_preferences):
    n = len(men_preferences) # number of men
    men_status = {man: None for man in men_preferences} # initialise the status of each man as a lad
    men_list = {man: men_preferences[man]['list'][:] for man in men_preferences} # copy the preference lists of men (used for proposing to women)
    women_engaged = {} # keep track of engaged couples (woman: man)
    men_index = {man: 0 for man in men_preferences} # initialise the index of each man's list (used for proposing to women)
    active_men = list(men_preferences.keys()) # list of active men who have not yet proposed to all women on their list
    men_attempts = {man: 0 for man in men_preferences} # keep track of the number of attempts each man has made to propose

    while active_men:
        # get the first man on the active list
        man = active_men[0]
        
        # get the first man's preference list
        woman_list = men_preferences[man]['list']

        # check for an empty preference list
        # check if the index of the current man in his preference list exceeds the length of the list
        if men_index[man] >= len(woman_list):
            # check if this is the first attempt for the man (men_attempts[man] == 0)
            if men_attempts[man] == 0:
                # copy the original preference list of the man to his current list (men_list[man])
                men_list[man] = men_preferences[man]['list'][:]
                # increment the attempts counter for the man
                men_attempts[man] += 1
                # check if this is the second attempt for the man
                if men_attempts[man] == 2:
                    # remove the man from the list of active men (he becomes an old bachelor)
                    active_men.remove(man)
            else:
                # remove the man from the list of active men (he becomes an old bachelor)
                active_men.remove(man)
            # continue to the next iteration of the while loop
            continue

        # get the first woman from the man's preference list
        woman = woman_list[men_index[man]][0]

        # woman is currently not engaged, so they become engaged
        # if a woman is maiden (then she will not be in the engaged list)
        if woman not in women_engaged:
            # change the status of man from None to the woman he has just been engaged to
            men_status[man] = woman
            # add the engagement to the women_engaged dictionary
            women_engaged[woman] = man
            # pop the man out of the active list
            active_men.pop(0)
        
        # woman is married to someone else already, so next logic
        else:
            # get the fiance she is already engaged to
            current_fiance = women_engaged[woman]
            # preference ranks of all the man in women's list
            woman_pref_rank = women_preferences[woman]['list_rank']

            # case 1: ranks are different
            # compare the rank of the new man to current fiance
            if woman_pref_rank[man] < woman_pref_rank[current_fiance]:
                # woman prefers this man over her current fiance, so they become angaged
                # so, change the new man status to married to woman
                men_status[man] = woman
                # update women engaged
                women_engaged[woman] = man
                # remove the man from the active list
                active_men.pop(0)
                # add the current fiance back to active men
                active_men.append(current_fiance)
                # change the status of the current fiance to None
                men_status[current_fiance] = None
                # + 1 to current  fiance men index (basically, changing the women index)
                men_index[current_fiance] += 1

                if men_attempts[current_fiance] == 2:
                    active_men.remove(current_fiance)

            # case 2: ranks are same (there is a tie)
            elif woman_pref_rank[man] == woman_pref_rank[current_fiance]:
                # woman has two men with the same rank, perfer bachelor over lad
                if men_attempts[man] == 1 and men_attempts[current_fiance] == 0:
                    # woman prefers the bachelor over the lad, so they become engaged
                    men_status[man] = woman
                    women_engaged[woman] = man
                    # remove the man from the active list
                    active_men.pop(0)
                    # add the current fiance to the active list
                    active_men.append(current_fiance)
                    # change the current men status to None
                    men_status[current_fiance] = None
                    # + 1 to current fiance men index
                    men_index[current_fiance] += 1
                
                # man is a lad and current fiance is a bachelor
                elif men_attempts[man] == 0 and men_attempts[current_fiance] == 1:
                    # increase the index of man
                    men_index[man] += 1
                
                elif men_attempts[man] == 0 and men_attempts[current_fiance] == 0:
                    # increase the index of man
                    men_index[man] += 1
            
            # move to the next woman in the list
            else:
                men_index[man] += 1
        
    return men_status, women_engaged

"""
men_preferences = {'m1': {'list': [['w2'], ['w5'], ['w1'], ['w3']], 'list_rank': {'w2': 1, 'w5': 2, 'w1': 3, 'w3': 4}}, 'm2': {'list': [['w1']], 'list_rank': {'w1': 1}}, 'm3': {'list': [['w2'], ['w3'], ['w4']], 'list_rank': {'w2': 1, 'w3': 2, 'w4': 3}}, 'm4': {'list': [['w2'], ['w3']], 'list_rank': {'w2': 1, 'w3': 2}}, 'm5': {'list': [['w3'], ['w4'], ['w5'], ['w1'], ['w2']], 'list_rank': {'w3': 1, 'w4': 2, 'w5': 3, 'w1': 4, 'w2': 5}}}

women_preferences = {'w1': {'list': [['m1'], ['m5', 'm2']], 'list_rank': {'m1': 1, 'm5': 2, 'm2': 2}}, 'w2': {'list': [['m1', 'm4'], ['m5', 'm3']], 'list_rank': {'m1': 1, 'm4': 1, 'm5': 2, 'm3': 2}}, 'w3': {'list': [['m1', 'm4'], ['m5'], ['m3']], 'list_rank': {'m1': 1, 'm4': 1, 'm5': 2, 'm3': 3}}, 'w4': {'list': [['m3'], ['m5']], 'list_rank': {'m3': 1, 'm5': 2}}, 'w5': {'list': [['m5', 'm1']], 'list_rank': {'m5': 1, 'm1': 1}}}

men_status, women_engaged = gsa1(men_preferences, women_preferences)

print(f"Men_status: {men_status}")

print(f"Women_engaged: {women_engaged}")
"""