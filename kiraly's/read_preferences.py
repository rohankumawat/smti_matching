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

    for i in range(n_men+1, len(lines)):
        line = lines[i].strip()
        woman_id, prefs = line.split(':')
        
        tied_prefs = []
        ongoing_tie = False

        for char in prefs:
            if char.isdigit() and not ongoing_tie:
                tied_prefs.append([char])
            elif char[0] == '(':
                tie = []
                ongoing_tie = True
            elif char.isdigit() and ongoing_tie:
                tie.append(char)
            elif char[-1] == ')':
                ongoing_tie = False
                tied_prefs.append(tie)
        
        women_preferences[woman_id] = tied_prefs

    return men_preferences, women_preferences

# You can now read the file, initialize men and women, and execute the GSA1 algorithm
filename = "examples/smi_ties1.txt"
men_prefs, women_prefs = read_file(filename)

men_dict = {man_id: Man(man_id) for man_id in men_prefs}
women_dict = {woman_id: Woman(woman_id) for woman_id in women_prefs}

for man_id, prefs in men_prefs.items():
    men_dict[man_id].preferences = prefs

for woman_id, prefs in women_prefs.items():
    women_dict[woman_id].preferences = prefs

print(men_prefs)
print(women_prefs)

matches = gsa1(men_dict, women_dict)

print(matches)
