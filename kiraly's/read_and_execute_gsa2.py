import os
import time
from gsa2 import gsa2, Man, Woman
from stability_checker import is_stable

def read_preferences(file_path):
    with open(file_path, 'r') as file:
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

def execute_gsa2_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            men_prefs, women_prefs = read_preferences(file_path)

            print(f"Executing Kiraly's GSA2 on file: {filename}", file=output_file)
            start_time = time.time()
            matches = gsa2(men_prefs, women_prefs)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time: .20f} seconds\n", file=output_file)
            print(f"Resulting matches: {matches}\n", file=output_file)

            men_prefs, women_prefs = read_preferences(file_path)
            blocking_pairs = check_blocking_pairs(men_prefs, women_prefs, matches)

            men_count, women_count = len(men_prefs), len(women_prefs)
            match_count = len(matches)

            print(f"Men Count: {men_count}, Women Count: {women_count}.", file=output_file)
            print(f"Matchings: {match_count}.", file=output_file)

            if blocking_pairs:
                print("Blocking pairs exist:\n", file=output_file)
            for pair in blocking_pairs:
                print(pair, "\n", file=output_file)
            else:
                print("No blocking pairs found.\n", file=output_file)

if __name__ == "__main__":
    directory_path = "./instances"
    output_file_path = "./output_gsa2.txt"
    execute_gsa2_on_files(directory_path)