import re

def insert_spaces(text):

    pattern = r'([a-z])(?=[A-Z])'
    
    
    result = re.sub(pattern, r'\1 ', text)
    
    return result

test_cases = ["PythonExercises", "CamelCaseIsCool", "ILovePython"]

for test in test_cases:
    print(f"Исходная: {test:20} -> С пробелами: {insert_spaces(test)}")