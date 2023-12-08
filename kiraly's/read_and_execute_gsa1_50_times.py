import copy
import os
from gsa1 import gsa1
from new_algorithm_one import new_algorithm
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

def execute_gsa1_50_times(men_prefs, women_prefs):

  best_size = 0
  best_matching = {}
  
  for i in range(100):
  
    men, women = new_algorithm(copy.deepcopy(men_prefs), copy.deepcopy(women_prefs))
    
    men_status = {
                man:details['engaged_to'] for man, details in men.items() 
                if 'engaged_to' in details
            }
    
    current_size = len([id for id in men_status.values() if id])
    
    if current_size > best_size:
      best_size = current_size  
      best_matching = men_status
      
    print(f"Iteration {i}: Size {current_size}")
    
  print(f"Best size: {best_size}")
  
  return best_matching, best_size

def execute_gsa1_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            s = SMTIFileReader()
            s.read(file_path)
            men_preferences, women_preferences = s.men, s.women

            print(f"Executing Kiraly's GSA1 on file: {filename}", file=output_file)
            best_match, best_size = execute_gsa1_50_times(men_preferences, women_preferences)
            # blocking_pairs = check_blocking_pairs(men_preferences, women_preferences, men_status, women_engaged)
            print(f"Best match: {best_match}\n", file=output_file)
            print(f"Best size: {best_size} \n", file=output_file)

if __name__ == "__main__":
    directory_path = "../experiments/general_smti/large_instances/instances_size_1000"  # Adjust the path as needed
    output_file_path = "../experiments/general_smti/results/new_algorithm_100_times/new_algo_model_size_1000.txt"  # Adjust the path as needed
    execute_gsa1_on_files(directory_path)