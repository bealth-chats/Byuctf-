import re

flag_parts = {}

# OCR part 1
try:
    with open('inception.png', 'rb') as f:
        pass
except:
    pass

# We have OCR result already: byuctf{wh4t_  (or something similar, we need to inspect it more closely but it looks like byuctf{wh4t_)
# Let's fix the typo manually if tesseract missed it.
flag_parts[1] = 'byuctf{wh4t_'

with open('_inception.extracted/data.bin', 'r') as f:
    text = f.read()
    match = re.search(r'flag part 2\s*={32}\s*(\S+)\s*={32}', text)
    if match:
        flag_parts[2] = match.group(1)

with open('_inception.extracted/4F3', 'r') as f:
    text = f.read()
    match = re.search(r'\(flag part 3\).*?\(_fr3ak}\)', text, re.DOTALL)
    if match:
        flag_parts[3] = '_fr3ak}'

print("Flags parsed:")
print(flag_parts)
print("Flag:", "".join([flag_parts[i] for i in sorted(flag_parts.keys())]))
