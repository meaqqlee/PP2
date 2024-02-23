# Python RegEx exercises

# Match 'a' followed by zero or more 'b's
pattern1 = 'ab*'

# Match 'a' followed by two to three 'b's
pattern2 = 'ab{2,3}'

# Find sequences of lowercase letters joined with a underscore
pattern3 = '[a-z]+_[a-z]+'

# Find sequences of one upper case letter followed by lower case letters
pattern4 = '[A-Z][a-z]+'

# Match 'a' followed by anything, ending in 'b'
pattern5 = 'a.*b$'

# Replace all occurrences of space, comma, or dot with a colon
pattern6 = '[\s,.]'

# Convert snake case string to camel case string
def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

# Split a string at uppercase letters
pattern7 = '[A-Z][^A-Z]*'

# Insert spaces between words starting with capital letters
def insert_spaces(s):
    return ''.join([' ' + c if c.isupper() else c for c in s]).lstrip()

# Convert camel case string to snake case
def camel_to_snake(camel_str):
    return ''.join(['_' + c.lower() if c.isupper() else c for c in camel_str]).lstrip('_')

# Testing the functions
print(snake_to_camel("hello_world"))
print(insert_spaces("HelloWorld"))
print(camel_to_snake("HelloWorld"))
