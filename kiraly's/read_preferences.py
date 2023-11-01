from gsa1 import gsa1, Man, Woman

def read_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    n_men, n_women = map(int, lines[0].split())
    men_preferences = {}
    women_preferences = {}

    for i in range(1, n_men+1):
        man_id, *prefs = lines[i].split()
        men_preferences[man_id[:-1]] = prefs

    for i in range(n_men+1, n_men+n_women+1):
        woman_id, *prefs = lines[i].split()
        women_preferences[woman_id[:-1]] = [p.split() for p in ' '.join(prefs).replace('(', ' ').replace(')', ' ').split()]

    return men_preferences, women_preferences

# You can now read the file, initialize men and women, and execute the GSA1 algorithm
filename = "examples/smi_ties0.txt"
men_prefs, women_prefs = read_file(filename)

men_dict = {man_id: Man(man_id) for man_id in men_prefs}
women_dict = {woman_id: Woman(woman_id) for woman_id in women_prefs}

for man_id, prefs in men_prefs.items():
    men_dict[man_id].preferences = prefs

for woman_id, prefs in women_prefs.items():
    women_dict[woman_id].preferences = prefs

print(women_prefs)
'''
matches = gsa1(men_dict, women_dict)

print(matches)
'''