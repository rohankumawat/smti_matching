import os
from instanceGenerator import StableMarriageInstance

def generate_and_save_instances(num_instances):
    instance_folder = "instances"
    os.makedirs(instance_folder, exist_ok=True)

    for i in range(num_instances):
        s = StableMarriageInstance(50)  # Adjust the size as needed
        instance_filename = os.path.join(instance_folder, f"instance_{i}.txt")
        s.smi_ties(1, 50, 0, 0.2)  # Modify parameters as needed
        s.write_to_file(instance_filename)
        print(f"Instance {i + 1} saved as {instance_filename}")

if __name__ == "__main__":
    num_instances = 100  # Change this to the number of instances you want to generate
    generate_and_save_instances(num_instances)
    print(f"{num_instances} instances generated and saved in the 'instances' folder.")