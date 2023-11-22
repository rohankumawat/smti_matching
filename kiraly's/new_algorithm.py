"""
While there exists an active man m, he proposes to his favorite woman w.
- if w accepts his proposal, they become engaged.
- if w rejects his proposal, m deltes w from his list.

When a woman w gets a new proposal from man m
- she always accepts this proposal if she is a "maiden" or a "flighty" woman".
- she also accepts this proposal, if she prefers m to her current fiance. 
- otherwise, she rejects m.

If w accepted m, then she rejects her previous fiance,
- if there was one(breaks off her engagement), and becomes engaged to m.

If m was engaged to a woman w and later w rejects him, 
- then m becomes active again, and deletes w from his list,
- except if m is uncertain, in this case m keeps w on the list.

If the list of m becomes empty for the first time, 
- he turns into a bachelor, 
- his original list is recovered,
- and he reactivates himself.

If the list of m becomes empty for the second time, 
- he will turn into an old bachelor and will remain inactive forever.
"""

def check_uncertain(man, woman, preferences):

  if men[man]['status'] == 'lad' and women[woman]['status'] == 'engaged':

    for w in men[man]['list']:
     if preferences[man]['list_rank'][w] >= preferences[man]['list_rank'][woman]:
        men[man]['uncertain'] = True  
        women[woman]['flighty'] = True
        break

  return men[man]['uncertain']

def propose(man, woman):
    women[woman]['engaged_to'] = man
    women[woman]['status'] = 'engaged'
    men[man]['engaged_to'] = woman
    men[man]['active'] = False

    uncertain = check_uncertain(man, woman, preferences)


def new_algorithm(men_preferences, women_preferences):
    # initialise all men to be lad and women to be maiden
    men = {man: {'status': 'lad', 'uncertain': False, 'active': True, 'engaged': None} for man in men_preferences}
    women = {woman: {'status': 'maiden', 'flighty': False, 'engaged_to': None} for woman in women_preferences}

    # active men
    active_men = [man for man in men if men[man]['active'] == True]
    # men index
    men_index = {man: 0 for man in men_preferences}
    # men attempts
    men_attempts = {man: 0 for man in men_preferences}
    # men list
    men_list = {man: men_preferences[man]['list'][:] for man in men_preferences}
    
    while active_men:
        # get the first active man from the active_men list
        man = active_men[0]

        # get the first man's preference list
        woman_list = men_preferences[man]['list']

        # check for an empty preference list
        # check if the index of the current man in his preference list is exceeds the length of the list
        if men_index[man] >= len(woman_list):
            # check if this is the first attempt for the man
            if men_attempts[man] == 0:
                # copy the original preference list of the man to his current list
                men_list[man] = men_preferences[man]['list'][:]
                # increment the attempts counter for the man
                men_attempts[man] += 1
                # check if this is the second attempt for the man
                if men_attempts[man] == 2:
                    # remove the man from the list of active men (he becomes an old bachelor)
                    active_men.remove(man)
                    if men[man]['uncertain'] == True:
                        men[man]['uncertain'] == False
            else:
                # remove the man from the list of active men (he becomes an old bachelor)
                active_men.remove(man)
                if men[man]['uncertain'] == True:
                    men[man]['uncertain'] == False
            # contine to the next iteration of the while loop
            continue

        # get the first woman from the man's preference list
        woman = woman_list[men_index[man]][0]

        # get the next woman from the list to check if there is a tie or not
        next_woman = woman_list[men_index[man]+1][0]

        # check if there is a tie
        if men_preferences[man]['list_rank'][woman] == men_preferences[man]['list_rank'][next_woman]:
            if women[woman]['status'] == 'maiden' and women[next_woman]['status'] == 'engaged':
                propose(man, woman)
            elif women[next_woman]['status'] == 'maiden' and women[woman]['status'] == 'engaged':
                propose(man, next_woman)
                men_index[man] += 1 # increment since next woman was proposed to

        # if the woman is maiden / flighty
        if women[woman]['status'] == 'maiden' or women[woman]['flighty'] == True:
            # engagement
            propose(man, woman)
            # pop the man out of the active list
            active_men.pop(0)
        
        # she already has a fiance
        else:
            # get the current fiance
            current_fiance = women[woman]['engaged_to']
            # preference ranks of all the man in women's list
            woman_pref_rank = women_preferences[woman]['list_rank']

            # case 1: ranks are different
            # compare the rank of the new man to current fiance
            if woman_pref_rank[man] < woman_pref_rank[current_fiance]:
                # woman prefers this man over her current fiance, so they become enaged
                # so, change the new man status to married to woman
                propose(man, woman)
                # remove the man from the active list
                active_men.pop(0)
                # woman rejects the current fiance
                if men[current_fiance]['uncertain']:
                    # keep woman in man's list
                    active_men.append(current_fiance)
                    men[current_fiance]['active'] = True
                    woman_list.remove(woman)
                    woman_list.append(woman)
                    men_index[current_fiance] += 1
                else:
                    # remove woman from man's list / increase the index
                    active_men.append(current_fiance)
                    men[current_fiance]['active'] = True
                    men_index[current_fiance] += 1
            
            # case 2: ranks are same
            elif woman_pref_rank[man] == woman_pref_rank[current_fiance]:
                # woman has two men with the same rank, prefer bachelor over lad
                if men_attempts[man] == 1 and men_attempts[current_fiance] == 0:
                    # woman prefers the bachelor over the lad
                    propose(man, woman)
                    active_men.pop(0)
                    # woman rejects the current fiance
                    if men[current_fiance]['uncertain']:
                        # keep woman in man's list
                        active_men.append(current_fiance)
                        men[current_fiance]['active'] = True
                        woman_list.remove(woman)
                        woman_list.append(woman)
                        men_index[current_fiance] += 1
                    else:
                        # remove woman from man's list / increase the index
                        active_men.append(current_fiance)
                        men[current_fiance]['active'] = True
                        men_index[current_fiance] += 1
                
                # man is a lad and current fiance is a bachelor
                elif men_attempts[man] == 0 and men_attempts[current_fiance] == 1:
                    # increase the index of man
                    men_index[man] += 1

                elif men_attempts[man] == 0 and men_attempts[current_fiance] == 0:
                    # increase the index of man
                    men_index[man] += 1
            
            else:
                men_index[man] += 1
    
    return men, women