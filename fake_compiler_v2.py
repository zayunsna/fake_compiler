

import random
import time
import argparse

def load_words(file_path):
    with open(file_path, 'r') as file:
        # Filter out short words and comments
        words = [w.strip() for w in file.read().splitlines() if len(w.strip()) > 2 and not w.startswith('#')]
    return words

def generate_realistic_identifier(words):
    """Combines words into realistic programming identifiers."""
    patterns = [
        lambda w1, w2: f"{w1.capitalize()}{w2.capitalize()}",  # PascalCase
        lambda w1, w2: f"{w1.lower()}{w2.capitalize()}",      # camelCase
        lambda w1, w2: f"{w1.lower()}_{w2.lower()}",          # snake_case
        lambda w1, w2: f"{w1.capitalize()}::{w2.lower()}",     # Class::method
        lambda w1, w2: f"g_{w1.lower()}_{w2.lower()}",       # global_variable
        lambda w1, w2: f"m_{w1.capitalize()}{w2.capitalize()}", # memberVariable
        lambda w1, w2, w3: f"{w1.capitalize()}{w2.capitalize()}{w3.capitalize()}",
        lambda w1, w2, w3: f"{w1.lower()}_{w2.lower()}_{w3.lower()}",
    ]

    pattern = random.choice(patterns)
    num_words = 3 if 'w3' in pattern.__code__.co_varnames else 2
    
    chosen_words = [random.choice(words) for _ in range(num_words)]
    
    return pattern(*chosen_words)

def generate_file_list(words, num_files=10):
    extensions = ['cpp', 'h', 'hpp', 'inl']
    return [f"{generate_realistic_identifier(words)}.{random.choice(extensions)}" for _ in range(num_files)]

def generate_dependency_paths(words, num_deps=3):
    base_dirs = ["include", "src", "lib", "third_party", "modules", "core"]
    paths = []
    for _ in range(num_deps):
        # Generate more realistic, nested paths
        path_depth = random.randint(1, 4)
        path_parts = [random.choice(base_dirs)]
        for _ in range(path_depth):
            path_parts.append(generate_realistic_identifier(words).split('::')[0]) # Use the class/namespace part
        
        # Ensure the final part is a header file
        path_parts.append(f"{generate_realistic_identifier(words).split('::')[0]}.h")
        path = '/'.join(path_parts)
        paths.append(path)
    return paths

def generate_error_message(file, theme, words):
    line_number = random.randint(10, 200)
    identifier = generate_realistic_identifier(words)

    if theme == 'cl.exe':
        errors = [
            f"{file}({line_number}): error C2065: '{identifier}': undeclared identifier",
            f"{file}({line_number}): error C2143: syntax error: missing ';' before '}}'",
            f"{file}({line_number}): fatal error C1083: Cannot open include file: '{generate_realistic_identifier(words)}.h': No such file or directory",
            f"{file}({line_number}): error LNK2019: unresolved external symbol \"{identifier}\" referenced in function main"
        ]
    else:  # for g++ and clang
        errors = [
            f"{file}:{line_number}: undefined reference to `__{identifier}'",
            f"{file}: In function `main':\n{file}:{line_number}: error: '{identifier}' was not declared in this scope",
            f"{file}:{line_number}: fatal error: {generate_realistic_identifier(words)}.h: No such file or directory\ncompilation terminated.",
            f"/usr/bin/ld: {generate_realistic_identifier(words)}.o: in function `{generate_realistic_identifier(words)}':\n(.text+0x1e): undefined reference to `{identifier}'"
        ]
    return random.choice(errors)

def simulate_compilation(file_list, words, theme='g++'):
    total_files = len(file_list)
    error_probability = 0.2

    themes = {
        'g++': {'command': 'g++', 'options': '-c {file} -o {obj_file} -I. {dependencies}', 'color': '\033[92m'},
        'clang': {'command': 'clang', 'options': '-c {file} -o {obj_file} -I. {dependencies}', 'color': '\033[94m'},
        'cl.exe': {'command': 'cl.exe', 'options': '/c {file} /Fo{obj_file} /I. {dependencies}', 'color': '\033[96m'}
    }
    selected_theme = themes.get(theme, themes['g++'])
    error_color = '\033[91m'
    reset_color = '\033[0m'

    for i, file in enumerate(file_list, start=1):
        dependencies = ' '.join(generate_dependency_paths(words, random.randint(1, 4)))
        obj_ext = '.obj' if theme == 'cl.exe' else '.o'
        obj_file = file.split('.')[0] + obj_ext

        compile_command = f"{selected_theme['command']} {selected_theme['options'].format(file=file, obj_file=obj_file, dependencies=dependencies)}"
        progress = int((i / total_files) * 100)
        progress_str = f"{progress:3d}%"

        if random.random() < error_probability:
            error_message = generate_error_message(file, theme, words)
            print(f"{selected_theme['color']}[{progress_str}]{reset_color} {compile_command}")
            print(f"{error_color}{error_message}{reset_color}")
            print("make: *** [Makefile:12: all] Error 1")
            break
        else:
            print(f"{selected_theme['color']}[{progress_str}]{reset_color} {compile_command}")
        
        time.sleep(random.uniform(0.05, 0.3))
    else:
        obj_files = ' '.join([f.split('.')[0] + obj_ext for f in file_list])
        print(f"{selected_theme['color']}[100%]{reset_color} {selected_theme['command']} -o my_project {obj_files}")
        time.sleep(1.0)
        print("./my_project")
        # Final output logs
        for log in ["[INFO] Initializing system...", "[INFO] System initialized successfully."]:
            print(log)
            time.sleep(random.uniform(0.3, 0.6))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulate a realistic-looking compilation process.')
    parser.add_argument('--theme', type=str, default='g++', choices=['g++', 'clang', 'cl.exe'], help='Compiler theme to use.')
    parser.add_argument('--num_files', type=int, default=150, help='Number of files to simulate compiling.')
    args = parser.parse_args()

    words_file_path = 'words.txt'
    words = load_words(words_file_path)
    file_list = generate_file_list(words, num_files=args.num_files)
    simulate_compilation(file_list, words, theme=args.theme)
