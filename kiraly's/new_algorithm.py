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

def new_algorithm(men_preferences, women_preferences):
  # initialise all men to be lad and women to be maiden
  men = {man: {'status': 'lad', 'attempts': 0, 'uncertain': False, 'active': True} for man in men_preferences}
  women = {woman: {'status': 'maiden', 'flighty': False, 'engaged_to': None} for woman in women_preferences}

  # check uncertain logic

  # propose function
  def propose(man, woman):
    women[woman]['engaged_to'] = man
    women[woman]['status'] = 'engaged'
    men[man]['engaged_to'] = woman
    men[man]['active'] = False

    if men[man]['status'] == 'lad' and women[woman]['status'] == 'engaged':

      first_woman = men_list[man][0][0]
      highest_rank = men_preferences[man]['list_rank'][first_woman]
      
      tie_group = []
      
      for sublist in men_list[man]:
        w = sublist[0]
        if men_preferences[man]['list_rank'][w] == highest_rank:
          tie_group.append(w)
          
      if len(tie_group) > 1:
        men[man]['uncertain'] = True
      
      if men[man]['uncertain']:
        women[woman]['flighty'] = True
      

  # active men
  active_men = [man for man in men if men[man]['active'] == True]
  # men list
  men_list = {man: men_preferences[man]['list'][:] for man in men_preferences}

  while active_men:
    # get the first active man from the active_men list
    man = active_men[0]

    # get the first man's preference list from men_list
    woman_list = men_list[man]

    # check for empty preference list
    if len(woman_list) == 0:
      
      if men[man]['attempts'] == 0: 
        # first empty case
        men[man]['status'] = 'bachelor'
        men[man]['attempts'] += 1
        men[man]['uncertain'] = False
        # copy the original preference list of the man to his current list
        men_list[man] = men_preferences[man]['list'][:]
      
      elif men[man]['attempts'] == 1:
        # second empty case
        men[man]['status'] = 'old bachelor'
        men[man]['attempts'] += 1
        men[man]['uncertain'] = False
        men[man]['active'] = False
        men[man]['engaged_to'] = None
        active_men.remove(man)
      
      else:
        active_men.remove(man)
      
      # continue to the next iteration of the while loop
      continue
    
    # check how many woman are there
    if len(woman_list) > 1:
      # get the first woman from the man's preference list
      woman = woman_list[0][0]

      # get the next woman from the list to check if there is a tie or not
      next_woman = woman_list[1][0]

      # check if there is a tie
      if men_preferences[man]['list_rank'][woman] == men_preferences[man]['list_rank'][next_woman]:
        if women[woman]['status'] == 'maiden' and women[next_woman]['status'] == 'engaged':
          propose(man, woman)
          active_men.pop(0)
          continue
        elif women[next_woman]['status'] == 'maiden' and women[woman]['status'] == 'engaged':
          propose(man, next_woman)
          active_men.pop(0)
          continue

    # there if only one woman in the list
    else:
      woman = woman_list[0][0]
    
    # if the woman if maiden / flighty
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
          men_list[current_fiance].remove([woman])
          men_list[current_fiance].append([woman])
        else:
          # remove the woman
          active_men.append(current_fiance)
          men[current_fiance]['active'] = True
          men_list[current_fiance].remove([woman])
      
      # case 2: ranks are same
      elif woman_pref_rank[man] == woman_pref_rank[current_fiance]:
        # woman has two men with the same rank, prefer bachelor over lad
        if men[man]['attempts'] == 1 and men[current_fiance]['attempts'] == 0:
          # woman prefers the bachelor over the lad
          propose(man, woman)
          active_men.pop(0)
          # woman rejects the current fiance
          if men[current_fiance]['uncertain']:
            # keep woman in man's list
            active_men.append(current_fiance)
            men[current_fiance]['active'] = True
            men_list[current_fiance].remove([woman])
            men_list[current_fiance].append([woman])
          else:
            # remove the woman
            active_men.append(current_fiance)
            men[current_fiance]['active'] = True
            men_list[current_fiance].remove([woman])
        
        # man is a lad and current fiance is a bachelor
        elif men[man]['attempts'] == 0 and men[current_fiance]['attempts'] == 1:
          # delete the woman from the list
          if men[man]['uncertain']:
            # keep woman in man's list
            men_list[man].remove([woman])
            men_list[man].append([woman])
          else:
            # remove the woman
            men_list[man].remove([woman])
        
        # both man are bachelors
        elif men[man]['attempts'] == 1 and men[current_fiance]['attempts'] == 1:
          # delete the woman from the list
          if men[man]['uncertain']:
            # keep woman in man's list
            men_list[man].remove([woman])
            men_list[man].append([woman])
          else:
            # remove the woman
            men_list[man].remove([woman])
        
        # both man are lad
        elif men[man]['attempts'] == 0 and men[current_fiance]['attempts'] == 0:
          # delete the woman from the list
          if men[man]['uncertain']:
            # keep woman in man's list
            men_list[man].remove([woman])
            men_list[man].append([woman])
          else:
            # remove the woman
            men_list[man].remove([woman])
        
      else:
        # delete the woman from the list
        if men[man]['uncertain']:
          # keep woman in man's list
          men_list[man].remove([woman])
          men_list[man].append([woman])
        else:
          # remove the woman
          men_list[man].remove([woman])
  
  return men, women

"""
men_preferences = {'m1': {'list': [['w9'], ['w5'], ['w1'], ['w8'], ['w3'], ['w4'], ['w7']], 'list_rank': {'w9': 1, 'w5': 2, 'w1': 3, 'w8': 4, 'w3': 5, 'w4': 6, 'w7': 7}}, 'm2': {'list': [['w2']], 'list_rank': {'w2': 1}}, 'm3': {'list': [['w4'], ['w9'], ['w1'], ['w2'], ['w3'], ['w6'], ['w5'], ['w7']], 'list_rank': {'w4': 1, 'w9': 2, 'w1': 3, 'w2': 4, 'w3': 5, 'w6': 6, 'w5': 7, 'w7': 8}}, 'm4': {'list': [['w2'], ['w1'], ['w9'], ['w7']], 'list_rank': {'w2': 1, 'w1': 2, 'w9': 3, 'w7': 4}}, 'm5': {'list': [['w3'], ['w7'], ['w5'], ['w1'], ['w6']], 'list_rank': {'w3': 1, 'w7': 2, 'w5': 3, 'w1': 4, 'w6': 5}}, 'm6': {'list': [['w6'], ['w2'], ['w3'], ['w8'], ['w10'], ['w9'], ['w7'], ['w4']], 'list_rank': {'w6': 1, 'w2': 2, 'w3': 3, 'w8': 4, 'w10': 5, 'w9': 6, 'w7': 7, 'w4': 8}}, 'm7': {'list': [['w8'], ['w10'], ['w3'], ['w5'], ['w2'], ['w9'], ['w1'], ['w7'], ['w4']], 'list_rank': {'w8': 1, 'w10': 2, 'w3': 3, 'w5': 4, 'w2': 5, 'w9': 6, 'w1': 7, 'w7': 8, 'w4': 9}}, 'm8': {'list': [['w4'], ['w10']], 'list_rank': {'w4': 1, 'w10': 2}}, 'm9': {'list': [['w10']], 'list_rank': {'w10': 1}}, 'm10': {'list': [['w2'], ['w8']], 'list_rank': {'w2': 1, 'w8': 2}}}
women_preferences = {'w1': {'list': [['m4', 'm7', 'm5', 'm3', 'm1']], 'list_rank': {'m4': 1, 'm7': 1, 'm5': 1, 'm3': 1, 'm1': 1}}, 'w2': {'list': [['m7'], ['m4'], ['m2', 'm3', 'm6', 'm10']], 'list_rank': {'m7': 1, 'm4': 2, 'm2': 3, 'm3': 3, 'm6': 3, 'm10': 3}}, 'w3': {'list': [['m3', 'm5'], ['m7'], ['m6', 'm1']], 'list_rank': {'m3': 1, 'm5': 1, 'm7': 2, 'm6': 3, 'm1': 3}}, 'w4': {'list': [['m3', 'm1', 'm8'], ['m7', 'm6']], 'list_rank': {'m3': 1, 'm1': 1, 'm8': 1, 'm7': 2, 'm6': 2}}, 'w5': {'list': [['m5', 'm3', 'm1', 'm7']], 'list_rank': {'m5': 1, 'm3': 1, 'm1': 1, 'm7': 1}}, 'w6': {'list': [['m3', 'm5', 'm6']], 'list_rank': {'m3': 1, 'm5': 1, 'm6': 1}}, 'w7': {'list': [['m4'], ['m3', 'm1', 'm5', 'm7', 'm6']], 'list_rank': {'m4': 1, 'm3': 2, 'm1': 2, 'm5': 2, 'm7': 2, 'm6': 2}}, 'w8': {'list': [['m10', 'm6', 'm1'], ['m7']], 'list_rank': {'m10': 1, 'm6': 1, 'm1': 1, 'm7': 2}}, 'w9': {'list': [['m3', 'm7', 'm4'], ['m6'], ['m1']], 'list_rank': {'m3': 1, 'm7': 1, 'm4': 1, 'm6': 2, 'm1': 3}}, 'w10': {'list': [['m6'], ['m7', 'm9', 'm8']], 'list_rank': {'m6': 1, 'm7': 2, 'm9': 2, 'm8': 2}}}

men, women = new_algorithm(men_preferences, women_preferences)

men_status = {
    man:details['engaged_to'] for man, details in men.items() 
    if 'engaged_to' in details
}

women_engaged = {
    woman:details['engaged_to'] for woman, details in women.items() 
    if 'engaged_to' in details
}

print(f"Men_status: {men_status}")

print(f"Women_engaged: {women_engaged}")
"""