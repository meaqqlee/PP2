pattern1 = 'ab*'

pattern2 = 'ab{2,3}'

pattern3 = '[a-z]+_[a-z]+'

pattern4 = '[A-Z][a-z]+'

pattern5 = 'a.*b$'

pattern6 = '[\s,.]'

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

pattern7 = '[A-Z][^A-Z]*'

def insert_spaces(s):
    return ''.join([' ' + c if c.isupper() else c for c in s]).lstrip()

def camel_to_snake(camel_str):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in camel_str]).lstrip('_')

# Testing the functions
print(snake_to_camel("hello_world"))
print(insert_spaces("HelloWorld"))
print(camel_to_snake("HelloWorld"))

import re
test_strings = [
    "ab",    
    "abb",     
    "aab",       
    "aabb",     
    "aabb",     
    "abbb",    
    "word_word",
    "Word_word",  
    "aWord",  
    "aWordb",    
    "a Word,b.",  
    "helloWorld", 
]

for test_string in test_strings:
    if re.match('ab*', test_string):
        print(f"{test_string} match 1 pattern")

    if re.match('ab{2,3}', test_string):
        print(f"{test_string} match 2 pattern")

    if re.match('[a-z]+_[a-z]+', test_string):
        print(f"{test_string} match 3 pattern")

    if re.match('[A-Z][a-z]+', test_string):
        print(f"{test_string} match 4 pattern")

    if re.match('a.*b$', test_string):
        print(f"{test_string} match 5 pattern")

    if re.search('[\s,.]', test_string):
        print(f"{test_string} match 6 pattern")

    if re.search('[A-Z][^A-Z]*', test_string):
        print(f"{test_string} match 7 pattern")


