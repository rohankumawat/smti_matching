import os
import time
from gsa1 import gsa1, Man, Woman
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

        for i in range(n_men+1, n_men+n_women+1):
            woman_id, *prefs = lines[i].split()
            women_preferences[woman_id[:-1]] = [p.split() for p in ' '.join(prefs).replace('(', ' ').replace(')', ' ').split()]

        return men_preferences, women_preferences

def execute_gsa1_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            men_prefs, women_prefs = read_preferences(file_path)

            men_dict = {man_id: Man(man_id) for man_id in men_prefs}
            women_dict = {woman_id: Woman(woman_id) for woman_id in women_prefs}

            for man_id, prefs in men_prefs.items():
                men_dict[man_id].preferences = prefs

            for woman_id, prefs in women_prefs.items():
                women_dict[woman_id].preferences = prefs

            print(f"Executing Kiraly's GSA1 on file: {filename}", file=output_file)
            start_time = time.time()
            matches = gsa1(men_dict, women_dict)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time: .20f} seconds\n", file=output_file)
            print(f"Resulting matches: {matches}\n", file=output_file)

            # Converting matches to a list of tuples for the stability checker
            matching_tuples = [(man, woman) for man, woman in matches.items()]
            men_prefs, women_prefs = read_preferences(file_path)
            print(men_prefs)
            print(women_prefs)
            stable_pairs, blocking_pairs = is_stable(matching_tuples, men_prefs, women_prefs)

            print(f"Stable pairs: {stable_pairs}", file=output_file)
            print(f"Blocking pairs: {len(blocking_pairs)}", file=output_file)
            print("Blocking pairs details: ", file=output_file)
            
            for pair in blocking_pairs:
                print(f"  {pair}", file=output_file)
            print("\n", file=output_file)
            """
            if stable_pairs == len(matching_tuples):
                print(f"There are {str(stable_pairs)} stable pairs and {len(blocking_pairs)} blocking pairs.\n",)
            else:
                print(f"The matching is not stable. There are {len(blocking_pairs)} blocking pairs.\n")
                print("Blocking pairs: ", blocking_pairs, "\n")
            """



if __name__ == "__main__":
    directory_path = "./examples"  # Adjust the path as needed
    output_file_path = "./output.txt"  # Adjust the path as needed
    execute_gsa1_on_files(directory_path)