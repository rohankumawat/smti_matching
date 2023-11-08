import os
import time
from mcdermid import * 

def read_preferences(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        n_men, n_women = map(int, lines[0].split())
        men_preferences = {}
        women_preferences = {}

        for i in lines[1: int(n_men)+1]:
            line = i.strip().split(':')
            line2 = line[1].strip().split()

            man_id = line[0]

            tied_prefs = []
            ongoing_tie = False

            for char in line2:
                if char.isdigit() and not ongoing_tie:
                    tied_prefs.append([char])
                elif char[0] == '(':
                    tie = []
                    ongoing_tie = True
                    tie.append(char[1:])
                elif char.isdigit() and ongoing_tie:
                    tie.append(char)
                elif char[-1] == ")":
                    tie.append(char[:-1])
                    ongoing_tie = False
                    tied_prefs.append(tie)
            
            men_preferences[man_id] = tied_prefs
        
        for i in lines[int(n_men)+1:]:
            line = i.strip().split(':')
            line2 = line[1].strip().split()

            woman_id = line[0]
        
            tied_prefs = []
            ongoing_tie = False

            for char in line2:
                if char.isdigit() and not ongoing_tie:
                    tied_prefs.append([char])
                elif char[0] == '(':
                    tie = []
                    ongoing_tie = True
                    tie.append(char[1:])
                elif char.isdigit() and ongoing_tie:
                    tie.append(char)
                elif char[-1] == ')':
                    tie.append(char[:-1])
                    ongoing_tie = False
                    tied_prefs.append(tie)
        
            women_preferences[woman_id] = tied_prefs

        return n_men, n_women, men_preferences, women_preferences
"""
n_men, n_women, men_preferences, women_preferences = read_preferences('examples/instance_1.txt')

print(n_men)
print(men_preferences)
print(women_preferences)
"""
def execute_mcdermid_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            n_men, n_women, men_prefs, women_prefs = read_preferences(file_path)
            """
            men = []
            for i in range(1, n_men+1):
                men.append(str(i))
            """
            men = [str(i) for i in range(1, n_men+1)]
            women = [str(i) for i in range(1, n_women+1)]

            promoted_men = set() # assuming a list to keep track of promotions
            reactivated_men = set() # assuming a list to keep track of reactivations
            # list to keep track of current matching
            matching = []
            # track the stalled and exhausted man
            stalled_men = set()
            exhausted_men = set()

            print(f"Executing McDermid's Algorithm on file: {filename}", file=output_file)
            start_time = time.time()
            # phase 1
            matching = phase1(men, women, men_prefs, women_prefs)

            # check if there are stalled men
            if stalled_men:
                # phase 2
                phase2_result = phase2(men, women, men_prefs, women_prefs, matching, stalled_men)
            
                if not phase2_result:
                    # phase 2 didn't yield any matches, proceed to phase 3
                    matching = phase3(matching, phase2_result)
            execution_time = time.time() - start_time

            print(f"Execution time: {execution_time: .20f} seconds \n", file=output_file)
            print(f"Resulting matches: {matching} \n", file=output_file)
            
if __name__ == "__main__":
    directory_path = "./instances"
    output_file_path = "./output_mcdermid.txt"
    execute_mcdermid_on_files(directory_path)
