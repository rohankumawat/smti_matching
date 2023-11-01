def is_stable(matching_tuples, men_preferences, women_preferences):
    """
    Checks whether the matching is stable considering rogue couples and unmatched individuals.

    Parameters:
    - matching_tuples (list): a list of tuples representing the matched pairs
    - men_preferences (dict): dictionary containing men's preferences
    - women_preferences (dict): dictionary containing women's preferences

    Returns:
    - stable_pairs (int): number of stable matches
    - blocking_pairs (list): list of tuples representing the blocking pairs
    """
    blocking_pairs = [] # list to store blocking pairs
    matching = dict(matching_tuples) # convert matching_tuples to a dictionary for easy lookup

    all_men = set(men_preferences.keys()) # set of all men
    all_women = set(women_preferences.keys()) # set of all women
    
    # Check for unmatched individuals
    matched_men = set(matching.keys()) # set of matched men
    matched_women = set(matching.values()) # set of matched women
    """
    if matched_men != all_men or matched_women != all_women:
        return (0, blocking_pairs) # return 0 stable pairs and an empty list of blocking pairs if there are unmatched individuals
    """

    # calculate the number of stable_pairs based on the matvching_tuples
    stable_pairs = len(matching_tuples) # total number of matches

    # Check for rogue couples / blocking pairs
    for man, woman in matching.items():
        current_woman_rank = men_preferences[man].index(woman) # Index of the current woman in man's preferences

        # check man's preferences to the left of the current woman
        for preferred_woman in men_preferences[man][:current_woman_rank]:
            her_man = next((m for m, w in matching.items() if w == preferred_woman), None) # find the man matched to the preffered woman
            if her_man and women_preferences[preferred_woman].index(man) < women_preferences[preferred_woman].index(her_man):
                blocking_pairs.append((man, preferred_woman)) # add a blocking pair
        
        current_man_rank = women_preferences[woman].index(man) # index of the current man in woman's preferences
        # check woman's preferences to the left of the current man
        for preferred_man in women_preferences[woman][:current_man_rank]:
            his_woman = matching.get(preferred_man) # find the woman matched to the preferred man
            if his_woman and men_preferences[preferred_man].index(woman) < men_preferences[preferred_man].index(his_woman):
                blocking_pairs.append((preferred_man, woman)) # add a blocking pair
                
    stable_pairs = len(matching_tuples) # total number of matches

    for man, woman in matching.items():
        stable_pairs.append((man, woman)) # add stable pairs to the list of stable pairs
    
    return stable_pairs, blocking_pairs # return the list of stable pairs and blocking pairs