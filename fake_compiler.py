import random
import time

def load_words(file_path):
    with open(file_path, 'r') as file:
        words = file.read().splitlines()
    return words

def random_word(words):
    return random.choice(words)

def generate_file_list(words, num_files=10):
    extensions = ['cpp', 'h', 'hpp']
    return [f"{random_word(words)}.{random.choice(extensions)}" for _ in range(num_files)]

def generate_dependency_paths(words, num_deps=3):
    base_dirs = ["include", "src", "lib", "third_party"]
    paths = []
    for _ in range(num_deps):
        path_parts = [random.choice(base_dirs)]
        for _ in range(random.randint(1, 10)): 
            path_parts.append(random_word(words))
        path_parts.append(f"{random_word(words)}.h")
        path = '/'.join(path_parts)
        paths.append(path)
    return paths

def simulate_compilation(file_list, words):
    total_files = len(file_list)
    error_probability = 0.01
    
    for i, file in enumerate(file_list, start=1):
        dependencies = ' '.join(generate_dependency_paths(words, random.randint(1, 4)))
        obj_file = file.replace('.cpp', '.o').replace('.h', '.o').replace('.hpp', '.o')
        compile_command = f"g++ -c {file} -o {obj_file} -I. {dependencies}"
        progress = int((i / total_files) * 100)
        progress_str = f"{progress:3d}%"
        
        if random.random() < error_probability:
            error_message = f"{file}: In function `int main()':\n{file}:12: undefined reference to `someUndefinedFunction()'"
            print(f"\033[92m[{progress_str}]\033[0m {compile_command}")
            print(error_message)
            print("make: *** [Makefile:12: all] Error 1")
            break
        else:
            print(f"\033[92m[{progress_str}]\033[0m {compile_command}")
        
        time.sleep(random.uniform(0.05, 0.3)) 

    else:
        obj_files = ' '.join(file.replace('.cpp', '.o').replace('.h', '.o').replace('.hpp', '.o') for file in file_list)
        print(f"\033[92m[100%]\033[0m g++ -o my_project {obj_files}")
        time.sleep(random.uniform(0.5, 1.0))

        print("./my_project")
        logs = [
            "[INFO] Initializing system...",
            "[INFO] Loading configuration...",
            "[INFO] Starting main services...",
            "[INFO] System initialized successfully."
        ]
        for log in logs:
            print(log)
            time.sleep(random.uniform(0.3, 0.6))

if __name__ == "__main__":
    words_file_path = 'words.txt'
    words = load_words(words_file_path)
    #### User Input ####
    # num_files : Int type Parameter
    #           : This param will control the total time of this fake compiling.
    file_list = generate_file_list(words, num_files=119)
    simulate_compilation(file_list, words)
