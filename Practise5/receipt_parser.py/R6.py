import re

def replace_with_colon(text):
    pattern = r'[ ,.]' 
    
    result = re.sub(pattern, ':', text)
    return result

test_text = "Python Exercises, PHP exercises. C# Exercises"

final_text = replace_with_colon(test_text)

print("Исходный текст:", test_text)
print("Результат:     ", final_text)