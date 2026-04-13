

new_string = '''\
    
    
    
    
    
hello world

this is the content of the string
'''

result = new_string.split("\n")[0].split()
if len(result) > 3:
    final_string = " ".join(result[:3]) + "..."
else:
    final_string = " ".join(result)
print(final_string)