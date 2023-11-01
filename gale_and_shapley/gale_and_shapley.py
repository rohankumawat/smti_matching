def gale_shapley(men_preferences, women_preferences):
    """
    Implementation of the Gale-Shapley algorithm.
    
    Parameters:
    - men_preferences (dict): Men's preferences of women
    - women_preferences (dict): Women's preferences of men
    
    Returns:
    - dict: Stable matchings of men and women
    """
    
    # Dictionary to store the current engagements
    engagements = {}
    
    # Dictionary to store the remaining women each man can propose to
    remaining_proposals = {man: list(women) for man, women in men_preferences.items()}
    
    # While there is a man who is free and hasn’t proposed to every woman
    while remaining_proposals:
        man, women = remaining_proposals.popitem()
        
        # Get the highest ranked woman from man's preference who he hasn’t proposed to yet
        woman = women.pop(0)
        
        fiance = engagements.get(woman)
        if not fiance:
            # If the woman is free, engage her with the man
            engagements[woman] = man
        else:
            # If she's already engaged, she might reconsider her choice
            if women_preferences[woman].index(man) < women_preferences[woman].index(fiance):
                # If she prefers the new man, update the engagement
                engagements[woman] = man
                # The dumped man will have a chance to propose again
                remaining_proposals[fiance] = men_preferences[fiance]
            else:
                # If she prefers her current fiance, the man will have a chance to propose again
                remaining_proposals[man] = women
        
    # Returning the engagements in a man-centric way
    return {v: k for k, v in engagements.items()}
"""
# Example usage:

men_preferences = {
    'm1': ['w1', 'w2', 'w3'],
    'm2': ['w2', 'w3', 'w1'],
    'm3': ['w3', 'w1', 'w2'],
}

women_preferences = {
    'w1': ['m1', 'm2', 'm3'],
    'w2': ['m2', 'm3', 'm1'],
    'w3': ['m3', 'm1', 'm2'],
}

print(gale_shapley(men_preferences, women_preferences))
"""