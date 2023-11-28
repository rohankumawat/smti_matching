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
  men = {man: {'status': 'lad', 'attempts': 0, 'uncertain': False, 'active': True, 'engaged_to': None} for man in men_preferences}
  women = {woman: {'status': 'maiden', 'flighty': False, 'engaged_to': None} for woman in women_preferences}

  # check uncertain logic

  # propose function
  def propose(man, woman):
    women[woman]['engaged_to'] = man
    women[woman]['status'] = 'engaged'
    men[man]['engaged_to'] = woman
    men[man]['active'] = False

    if men[man]['status'] == 'lad' and women[woman]['status'] == 'engaged':

      uncertain = False
      
      for pref_list in men_list[man]:
      
        for alternate_woman in pref_list:
        
          # Check if preferred, available, and not the fiancée
          if (men_preferences[man]['list_rank'][alternate_woman] < 
              men_preferences[man]['list_rank'][woman]
              and alternate_woman not in women_engaged):
                
            uncertain = True
            break
              
      if uncertain:
        men[man]['uncertain'] = True
      
      else:
        men[man]['uncertain'] = False

      if men[man]['uncertain']:
        women[woman]['flighty'] = True
      else:
        women[woman]['flighty'] = False
  
  def remove_woman(men_list, man, woman):
    men_list[man] = [
     sublist for sublist in (
         [] if woman in pref_list and len(pref_list)==1 
         else [w for w in pref_list if w != woman]  
         for pref_list in men_list[man])
     if sublist
  ]

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
        men[man]['engaged_to'] = None
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
    if len(woman_list) > 0:
      # get the first woman from the man's preference list
      first_pref_list = woman_list[0]
      woman = first_pref_list[0]

      if len(first_pref_list) > 1:
        # there is a tie
        second_woman = first_pref_list[1]
        if men_preferences[man]['list_rank'][woman] == men_preferences[man]['list_rank'][second_woman]:
          if women[woman]['status'] == 'maiden' and women[second_woman]['status'] == 'engaged':
            woman = woman
          elif women[woman]['status'] == 'engaged' and women[second_woman]['status'] == 'maiden':
            woman = second_woman
          elif women[woman]['status'] == 'maiden' and women[second_woman]['status'] == 'maiden':
            woman = woman
          elif women[woman]['status'] == 'engaged' and women[second_woman]['status'] == 'engaged':
            woman = woman

      else:
        woman = woman_list[0][0]

    # if the woman if maiden / flighty
    if women[woman]['status'] == 'maiden' or women[woman]['flighty'] == True:
      # engagement
      propose(man, woman)
      # pop the man out of the active list
      active_men.pop(0)
    
    elif women[woman]['flighty'] == True:
      # get the current fiance
      current_fiance = women[woman]['engaged_to']
      # engagement
      propose(man, woman)
      # pop the man out of the active list
      active_men.pop(0)
      # set the current fiance to be active again
      active_men.append(current_fiance)
      men[current_fiance]['active'] = True
      remove_woman(men_list, current_fiance, woman)
      men_list[current_fiance].append([woman])
      men[man]['engaged_to'] = None

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
          remove_woman(men_list, current_fiance, woman)
          men_list[current_fiance].append([woman])
        else:
          # remove the woman
          active_men.append(current_fiance)
          men[current_fiance]['active'] = True
          remove_woman(men_list, current_fiance, woman)

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
            remove_woman(men_list, current_fiance, woman)
            men_list[current_fiance].append([woman])
          else:
            # remove the woman
            active_men.append(current_fiance)
            men[current_fiance]['active'] = True
            remove_woman(men_list, current_fiance, woman)

        # man is a lad and current fiance is a bachelor
        elif men[man]['attempts'] == 0 and men[current_fiance]['attempts'] == 1:
          # delete the woman from the list
          if men[man]['uncertain']:
            # keep woman in man's list
            remove_woman(men_list, man, woman)
            men_list[man].append([woman])
          else:
            # remove the woman
            remove_woman(men_list, man, woman)

        # both man are bachelors
        elif men[man]['attempts'] == 1 and men[current_fiance]['attempts'] == 1:
          # delete the woman from the list
          if men[man]['uncertain']:
            # keep woman in man's list
            remove_woman(men_list, man, woman)
            men_list[man].append([woman])
          else:
            # remove the woman
            remove_woman(men_list, man, woman)

        # both man are lad
        elif men[man]['attempts'] == 0 and men[current_fiance]['attempts'] == 0:
          # delete the woman from the list
          if men[man]['uncertain']:
            # keep woman in man's list
            remove_woman(men_list, man, woman)
            men_list[man].append([woman])
          else:
            # remove the woman
            remove_woman(men_list, man, woman)

      else:
        # delete the woman from the list
        if men[man]['uncertain']:
          # keep woman in man's list
          remove_woman(men_list, man, woman)
          men_list[man].append([woman])
        else:
          # remove the woman
          remove_woman(men_list, man, woman)
  
  return men, women