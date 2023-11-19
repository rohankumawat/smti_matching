import os
import time
from gurobipy import *
from ip_model import SMTIWeakStability
from readFile import SMTIFileReader

def execute_ip_model_on_files(directory_path):
    with open(output_file_path, 'w') as output_file:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            s = SMTIWeakStability(file_path)
            print(f"Executing IP Model on file: {filename}", file=output_file)
            start_time = time.time()
            s.run_ip_model()
            execution_time = time.time() - start_time
            print(f"Execution time: {execution_time: .20f} seconds\n", file=output_file)
            print(f"Matching: {s.matching}", file=output_file)
            blocking_pairs = s.check_blocking_pairs()
            print(f"Blocking pair: {blocking_pairs} \n", file=output_file)

if __name__ == "__main__":
    directory_path = "../experiments/men_have_strictly_ordered_lists/large_instances/instances_size_500"
    output_file_path = "../experiments/men_have_strictly_ordered_lists/results/ip_model_size_500.txt"
    # execute_gsa1_on_files(directory_path)
    execute_ip_model_on_files(directory_path)