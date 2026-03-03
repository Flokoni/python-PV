def snake_to_camel(text):
    words = text.split('_')
    
    camel_string = words[0] + ''.join(word.capitalize() for word in words[1:])
    
    return camel_string

test_cases = ["hello_world", "convert_snake_case", "python_is_fun", "total_amount_sum"]

for test in test_cases:
    print(f"Snake Case: {test:20} -> Camel Case: {snake_to_camel(test)}")