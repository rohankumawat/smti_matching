def check_blocking_pairs(men_preferences, women_preferences, men_status, women_engaged):
    for man, woman in men_status.items():
        if woman is not None:
            assigned_woman = woman
            rank_assigned_woman = men_preferences[man]['list_rank'][assigned_woman]
            preferred_women = men_preferences[man]['list'][:rank_assigned_woman - 1] if rank_assigned_woman > 1 else []

            for tie in preferred_women:
                for new_woman in tie:
                    assigned_man = women_engaged[new_woman]
                    rank_assigned_man = women_preferences[new_woman]['list_rank'][assigned_man]
                    rank_man = women_preferences[new_woman]['list_rank'][man]

                    if rank_man < rank_assigned_man:
                        return True  # Blocking pair found
    
    return False  # No blocking pairs found
