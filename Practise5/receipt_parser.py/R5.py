import re

def match_a_anything_b(text):

    pattern = r'^a.*b$'
    
    if re.fullmatch(pattern, text):
        return "Совпадение! (Match)"
    else:
        return "Не подходит (No match)"


test_cases = ["ab", "axb", "a123b", "a____b", "abc", "ba", "a"]

for t in test_cases:
    print(f"Строка '{t}': {match_a_anything_b(t)}")