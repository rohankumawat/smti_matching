import os
import time
from gale_and_shapley import gale_shapley
from stability_checker import is_stable

def read_preferences(file_path):
    with open(file_path, 'r') as file:
        n, _ = map(int, file.readline().split())
        men_prefs = {}
        women_prefs = {}
        
        for _ in range(n):
            line = file.readline().split()
            man = int(line[0][:-1])
            prefs = list(map(int, line[1:]))
            men_prefs[man] = prefs
            
        for _ in range(n):
            line = file.readline().split()
            woman = int(line[0][:-1])
            prefs = list(map(int, line[1:]))
            women_prefs[woman] = prefs
        
        return men_prefs, women_prefs


def execute_gale_shapley_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            men_prefs, women_prefs = read_preferences(file_path)

            print(f"Executing Gale-Shapley on file: {filename}", file=output_file)
            start_time = time.time()
            matches = gale_shapley(men_prefs, women_prefs)
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time: .20f} seconds\n", file=output_file)
            print(f"Resulting matches: {matches}\n", file=output_file)

            # Converting matches to a list of tuples for the stability checker
            matching_tuples = [(man, woman) for man, woman in matches.items()]
            men_prefs, women_prefs = read_preferences(file_path)
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
    execute_gale_shapley_on_files(directory_path)