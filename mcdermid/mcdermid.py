from collections import defaultdict
import networkx as nx
import time

"""
Phase 1
"""
class Person:

    def __init__(self, name, preferences):
        self.name = name
        self.preferences = preferences
        self.partner = None    
        self.tie = 0
        self.promoted = False
        self.exhausted = False
        self.stalled = False

    def prefers(self, p1, p2):
        return self.preferences.index(p1) < self.preferences.index(p2)


class Matching:

    def __init__(self):
        self.pairs = []

    def add_pair(self, p1, p2):
        self.pairs.append((p1, p2))

    def remove_pair(self, p1, p2):
        self.pairs.remove((p1, p2))

    def get_partner(self, person):
        for pair in self.pairs:
            if person in pair:
                return pair[0] if pair[1] == person else pair[1]
        return None

def smti_phase1(men, women):
    
    matching = Matching()
    
    free_men = men[:]
    stalled_men = set()

    while free_men:
        m = free_men.pop(0)
        
        print("Considering man:", m.name)
        
        if m.exhausted:
            m.promoted = True
            m.exhausted = False
            m.tie = 0
            continue
            
        tie = m.preferences[m.tie]
        print("Current tie:", tie)
        
        tie_women = [w for w in tie if w not in map(lambda p: p.partner, women)]

        if not tie_women:
            print("Stalling man")
            stalled_men.add(m)
            m.tie += 1
            
        else:
            print("Proposing...")
            w = tie_women[0] 
            if w not in map(lambda p: p.partner, women):
                matching.add_pair(m, w)
                unstall_men(w, stalled_men, free_men)
            else: 
                m.exhausted = True
    return matching

def unstall_men(w, stalled_men, free_men):
    
  if not stalled_men:
    return

  for m in list(stalled_men): 
    if w in m.preferences[m.tie]:
      stalled_men.remove(m)
      free_men.append(m)

"""
Phase 2
"""

def construct_phase2_graph(men, women, matching):
    graph = nx.Graph()
    graph.add_nodes_from(men)
    graph.add_nodes_from(women)

    for w in women:
        if w not in map(lambda p: p.partner, men):
            graph.add_edges_from([(m, w) for m in men if w in m.preferences])

    return graph

def max_cardinality_matching(graph):
    return nx.max_weight_matching(graph)

# function to perform the second phase of the stable marriage algorithm
def smti_phase2(men, women, matching):
    graph = construct_phase2_graph(men, women, matching)
    N = max_cardinality_matching(graph)

    E = {w for w in women if w not in map(lambda p: p[1], N)}
    O = {m for m in men if m not in map(lambda p: p[0], N)}
    U = set(men) - O

    N0 = [(m, w) for (m, w) in N if m not in O or w not in E]

    if not N0:
        return smti_phase3(men, women, matching)

    for (m, w) in N0:
        # m proposes to w
        m.preferences.remove(m.tie)
        m.preferences.insert(0, [w])
        matching.add_pair(m, w)
        m.stalled = False

        if m in U:
            U.remove(m)

    return smti_phase1(men, women)

"""
Phase 3
"""
# funtion to perform the third phase of the stable marriage algorithm
def smti_phase3(men, women, matching):
    
  final_matching = Matching()
  
  for (m, w) in matching.pairs: 
    if (m, w) not in final_matching.pairs:
      final_matching.add_pair(m, w)

  return final_matching

# main function to execute the entire stable marriage
def stable_marriage_ti(men, women):
    
  matching = smti_phase1(men, women)
  
  if any(m.stalled for m in men):
    matching = smti_phase2(men, women, matching)

  matching = smti_phase3(men, women, matching)

  return matching