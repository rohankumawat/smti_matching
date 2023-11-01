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
    blocking_pairs = []
    matching = dict(matching_tuples)

    all_men = set(men_preferences.keys())
    all_women = set(women_preferences.keys())
    
    # Check for unmatched individuals
    matched_men = set(matching.keys())
    matched_women = set(matching.values())

    if matched_men != all_men or matched_women != all_women:
        return False

    # Check for rogue couples
    for man, woman in matching.items():
        current_woman_rank = men_preferences[man].index(woman)

        for preferred_woman in men_preferences[man][:current_woman_rank]:
            her_man = next((m for m, w in matching.items() if w == preferred_woman), None)
            if her_man and women_preferences[preferred_woman].index(man) < women_preferences[preferred_woman].index(her_man):
                blocking_pairs.append((man, preferred_woman))
        
        current_man_rank = women_preferences[woman].index(man)
        for preferred_man in women_preferences[woman][:current_man_rank]:
            his_woman = matching.get(preferred_man)
            if his_woman and men_preferences[preferred_man].index(woman) < men_preferences[preferred_man].index(his_woman):
                blocking_pairs.append((preferred_man, woman))
                
    stable_pairs = len(matching_tuples) - len(blocking_pairs)
    return stable_pairs, blocking_pairs
