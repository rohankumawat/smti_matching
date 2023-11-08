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


# class to represent a Man
class Man:
    def __init__(self, id):
        self.id = id
        self.preferences = [] # list of woman preferences
        self.proposed_to = set() # set to keep track of proposed woman
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
    def __init__(self, id):
        self.id = id
        self.preferences = [] # list of man preferences
        self.fiance = None # initially not engaged
    
    # function for a woman to receive a proposal from a man
    def receive_proposal(self, man, men_dict):
        if self.fiance is None:
            return True
        
        current_man = men_dict[self.fiance] # check if it's not NONE

        # preference comparison logic / ties
        if man.status == 'bachelor' and current_man.status == 'lad':
            return True
        elif man.status == 'lad' and current_man.status == 'bachelor':
            return False
        
        for preference in self.preferences:
            if man.id in preference:
                return True
            elif self.fiance in preference:
                return False

# Gale-Shapley Algorithm 1
def gsa1(men_dict, women_dict):
    active_men = list(men_dict.values())

    # while there are active men
    while active_men:
        man = active_men.pop(0)
        woman_id = man.propose() # man proposes to a woman
        print(man, woman_id)

        if woman_id:
            woman = women_dict[woman_id]

            # woman receives the proposal and makes a decision
            if woman.receive_proposal(man, men_dict):
                if woman.fiance:
                    prev_man = men_dict[woman.fiance]
                    prev_man.proposed_to.remove(woman_id)
                    active_men.append(prev_man)
                woman.fiance = man.id # woman becomes engaged to the man
            
            else:
                if man.status == 'lad':
                    man.status = 'bachelor'
                    man.proposed_to.clear()
                    active_men.append(man)
                elif man.status == 'bachelor':
                    man.status = 'old bachelor'
    
    # construct the matches (engagements)
    matches = {}
    for woman in women_dict.values():
        if woman.fiance:
            matches[woman.fiance] = woman.id
    
    return matches  # return the final stable matches
