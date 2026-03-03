import re

def camel_to_snake(text):

    pattern = r'([a-z0-9])([A-Z])'
    

    substituted = re.sub(pattern, r'\1_\2', text)
    
    return substituted.lower()


test_cases = ["camelCase", "pythonIsFun", "totalAmountSum", "HTTPResponseCode"]

for test in test_cases:
    print(f"Camel Case: {test:20} -> Snake Case: {camel_to_snake(test)}")