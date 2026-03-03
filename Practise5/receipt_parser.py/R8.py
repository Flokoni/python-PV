import re

def split_at_uppercase(text):

    pattern = r'(?=[A-Z])'
    
    
    result = re.split(pattern, text)
    
    return [s for s in result if s]

test_text = "PythonExercisesIsGreat"

split_result = split_at_uppercase(test_text)

print("Исходная строка:", test_text)
print("Результат:     ", split_result)