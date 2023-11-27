import os
import time
from new_algorithm import new_algorithm
from blocking_pair import check_blocking_pairs


class SMTIFileReader():
    def __init__(self):
        self.men = dict()
        self.women = dict()
        

    def read(self, filename):
        with open(filename) as I:
            I = I.readlines()
            instance_size = I[0].strip().split()
            men_size, women_size = instance_size
            # ..reading the men's preference list..
            for line in I[1:int(men_size) + 1]:
                line = line.strip().split(':')
                line2 = line[1].strip().split()
                m = f'm{line[0]}'
                m_list = []                
                ongoing_tie = False
                m_list_rank = {}
                w_rank = 1
                for char in line2:
                    if char.isdigit() and not ongoing_tie:
                        m_list.append([f'w{char}'])
                        m_list_rank[f'w{char}'] = w_rank
                        w_rank += 1
                    elif char[0]=='(':
                        tie = []
                        ongoing_tie = True
                        tie.append(f'w{char[1:]}')
                        m_list_rank[f'w{char[1:]}'] = w_rank
                    elif char.isdigit() and ongoing_tie:
                        tie.append(f'w{char}')
                        m_list_rank[f'w{char}'] = w_rank
                    elif char[-1] == ')':
                        tie.append(f'w{char[:-1]}')
                        m_list_rank[f'w{char[:-1]}'] = w_rank
                        m_list.append(tie)                                                
                        ongoing_tie = False
                        w_rank += 1
                self.men[m] = {"list": m_list, "list_rank": m_list_rank}
                        
                # print(m, self.men[m]) 
                # print()
                
            # ..reading the women's preference list..
            for line in I[int(men_size)+1: ]:
                line = line.strip().split(':')
                line2 = line[1].strip().split()
                w = f'w{line[0]}'                
                w_list = []                
                ongoing_tie = False
                w_list_rank = {}
                m_rank = 1
                for char in line2:
                    if char.isdigit() and not ongoing_tie:
                        w_list.append([f'm{char}'])
                        w_list_rank[f'm{char}'] = m_rank
                        m_rank += 1
                    elif char[0]=='(':
                        tie = []
                        ongoing_tie = True  
                        tie.append(f'm{char[1:]}')
                        w_list_rank[f'm{char[1:]}'] = m_rank
                    elif char.isdigit() and ongoing_tie:
                        tie.append(f'm{char}')
                        w_list_rank[f'm{char}'] = m_rank
                    elif char[-1] == ')':
                        tie.append(f'm{char[:-1]}')
                        w_list_rank[f'm{char[:-1]}'] = m_rank
                        w_list.append(tie)                                                
                        ongoing_tie = False
                        m_rank += 1
                self.women[w] = {"list": w_list, "list_rank": w_list_rank}
                # print(w, self.women[w])
                # print()
# s = SMTIFileReader()         
# s.read("in4.txt")

def execute_gsa1_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            s = SMTIFileReader()
            s.read(file_path)
            men_preferences, women_preferences = s.men, s.women

            print(f"Executing Kiraly's New Algorithm on file: {filename}", file=output_file)
            start_time = time.time()
            men, women = new_algorithm(men_preferences, women_preferences)
            execution_time = time.time() - start_time
            men_status = {
                man:details['engaged_to'] for man, details in men.items() 
                if 'engaged_to' in details
            }
            women_engaged = {
                woman:details['engaged_to'] for woman, details in women.items() 
                if 'engaged_to' in details
            }
            blocking_pairs = check_blocking_pairs(men_preferences, women_preferences, men_status, women_engaged)
            print(f"Execution time: {execution_time: .30f} seconds\n", file=output_file)
            print(f"Resulting matches: {men_status}\n", file=output_file)
            print(f"Blocking pair: {blocking_pairs} \n", file=output_file)

            """
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
            """
            if stable_pairs == len(matching_tuples):
                print(f"There are {str(stable_pairs)} stable pairs and {len(blocking_pairs)} blocking pairs.\n",)
            else:
                print(f"The matching is not stable. There are {len(blocking_pairs)} blocking pairs.\n")
                print("Blocking pairs: ", blocking_pairs, "\n")
            """


if __name__ == "__main__":
    directory_path = "../experiments/men_have_strictly_ordered_lists/small_instances/instances_size_100"  # Adjust the path as needed
    output_file_path = "../experiments/men_have_strictly_ordered_lists/results/new_algorithm_model_size_100.txt"  # Adjust the path as needed
    execute_gsa1_on_files(directory_path)