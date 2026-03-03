import re

def match_a_23b(text):
    
    pattern = r'^ab{2,3}$'
    
    if re.fullmatch(pattern, text):
        return "Совпадение! (Match)"
    else:
        return "Не подходит (No match)"


test_strings = ["ab", "abb", "abbb", "abbbb", "a", "ba"]

for s in test_strings:
    print(f"Строка '{s}': {match_a_23b(s)}")