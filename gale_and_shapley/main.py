from read_preferences import read_preferences
from gale_and_shapley import gale_shapley

# Reading preferences from a file
men_preferences, women_preferences = read_preferences('sm2.txt')

# Executing the Gale-Shapley algorithm
matching = gale_shapley(men_preferences, women_preferences)

# Output the result
print(matching)
