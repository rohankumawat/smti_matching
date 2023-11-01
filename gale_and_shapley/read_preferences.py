def read_preferences(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extracting the number of men and women from the first line
    num_men, num_women = map(int, lines[0].split())

    men_preferences = {}
    women_preferences = {}

    # Processing men's preferences
    for i in range(1, num_men+1):
        data = lines[i].split(':')
        man = int(data[0])
        preferences = list(map(int, data[1].split()))
        men_preferences[man] = preferences

    # Processing women's preferences
    for i in range(num_men+1, num_men+num_women+1):
        data = lines[i].split(':')
        woman = int(data[0])
        preferences = list(map(int, data[1].split()))
        women_preferences[woman] = preferences

    return men_preferences, women_preferences
"""
# Usage:
men_preferences, women_preferences = read_preferences('sm1.txt')
print(men_preferences)
print(women_preferences)
"""