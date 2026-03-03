import re

def find_underscored_sequences(text):

    pattern = r'[a-z]+_[a-z]+'
    
    matches = re.findall(pattern, text)
    return matches

test_text = "Check these: hello_world, Python_code, test_file_name, My_Data, abc_def_ghi"

results = find_underscored_sequences(test_text)

print("Найденные совпадения:")
print(results)