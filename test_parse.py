import re

with open('asm.txt', 'r') as f:
    lines = f.readlines()

for line in lines:
    if "mov    $0x270,%esi" in line:
        print(line)
        break

for i, line in enumerate(lines):
    if "1349:" in line:
        for j in range(10):
            print(lines[i+j].strip())
        break
