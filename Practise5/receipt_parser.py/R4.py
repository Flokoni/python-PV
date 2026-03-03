import re

def find_capitalized_words(text):
    
    pattern = r'[A-Z][a-z]+'
    
    matches = re.findall(pattern, text)
    return matches

test_str = "Apple, banana, Carrot, iPhone, Kazakhstan, NASA, Python"

results = find_capitalized_words(test_str)

print("Найдено последовательностей:")
print(results)