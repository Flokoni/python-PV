import re

def match_ab(text):
    # Шаблон: 'a' затем 'b' в количестве 0 или больше
    pattern = r'ab*'
    
    if re.fullmatch(pattern, text):
        return "Совпадение найдено! (Found a match!)"
    else:
        return "Не соответствует шаблону (Not a match)"

# Примеры для проверки:
test_cases = ["a", "ab", "abbb", "b", "ba", "abc"]

for test in test_cases:
    print(f"Строка '{test}': {match_ab(test)}")