import sys
import re

def count_letters_at_trigger_end(string):
    
    pattern = r'[a-zA-Z]+$'  
    matches = re.findall(pattern, string)

    if matches:
        return len(matches[0])
    else:
        return 0


graceID = sys.argv[1]
letters_number = count_letters_at_trigger_end(graceID)

first_part_of_id = re.sub("[^0-9]", "", graceID)
trigger_id = first_part_of_id
for i in range(0,letters_number):

    last = str(ord(graceID[-(letters_number-i)]) - 96)
    trigger_id =  trigger_id+last.zfill(2)

print(trigger_id)