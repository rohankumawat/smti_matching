# class to represent a Man
class Man:
    def __init__(self, id, preferences):
        self.id = id
        self.preferences = preferences # list of woman preferences
        self.proposed_to = set() # set to keep track of proposed women
        self.status = "lad" # initial status as "lad"

    # function for a man to propose to a woman based on preferences
    def propose(self):
        for woman_id in self.preferences:
            if woman_id not in self.proposed_to:
                self.proposed_to.add(woman_id)
                return woman_id
        return None

# class to represent a woman
class Woman:
    def __init__(self, id, preferences):
        self.id = id
        self.preferences = preferences # list of man preferences
        self.fiance = None # initially not engaged

    # function for a woman to receive a proposal from a man
    def receive_proposal(self, man, men_dict):
        if self.fiance is None:
            return True
        
        current_man = men_dict[self.fiance]

        # preference comparison logic / ties
        if man.status == "bachelor" and current_man.status == "lad":
            return True
        elif man.status == "lad" and current_man.status == "bachelor":
            return False
        
        for preference in self.preferences:
            if man.id in preference:
                return True
            elif self.fiance in preference:
                return False

# Gale-Shapley 2
def gsa2(men_prefs, women_prefs):
    men_dict = {}
    women_dict = {}

    # initialise men and women with their preferences
    for man_id, preferences in men_prefs.items():
        men_dict[man_id] = Man(man_id, preferences)

    for woman_id, preferences in women_prefs.items():
        women_dict[woman_id] = Woman(woman_id, preferences)

    active_men = list(men_dict.values())

    # keep track of the number of times a man's list becomes empty
    empty_lists_count = {man_id: 0 for man in active_men}

    while active_men:
        man = active_men.pop(0)

        # check if the man's list is empty for the second time
        if empty_lists_count[man.id] == 2:
            man.status = 'old bachelor'
            continue # skip this man, as he's now an old bachelor

        woman_id = man.propse() # man proposes to a woman

        if woman_id:
            woman = women_dict[woman_id]

            # woman receives the proposal and makes a decision
            if woman.receive_proposal(man, men_dict):
                if woman.fiance:
                    prev_man = men_dict[woman.fiance]
                    prev_man.proposed_to.remove(woman_id)
                    active_men.append(prev_man)
                woman.fiance = man.id # woman becomes engaged to the man

                # reset the mepty list count for this man
                empty_lists_count[man.id] = 0
            else:
                if man.status == "lad":
                    man.status = "bachelor"
                    man.proposed_to.clear()
                    active_men.append(man)
                    empty_lists_count[man.id] += 1
                elif man.status == "bachelor":
                    if not man.proposed_to:
                        man.status = "old_bachelor"
    
    # construct the matches (engagements)
    matches = {}
    for woman in women_dict.values():
        if woman.fiance:
            matches[woman.fiance] = woman.id
    
    return matches # return the final stable matches