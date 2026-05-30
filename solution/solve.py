with open('pickled.txt', 'r') as f:
    content = f.read().split()

binary_string = ''
for word in content:
    if word == 'rick':
        binary_string += '0'
    elif word == 'pickle':
        binary_string += '1'

bytes_list = []
for i in range(0, len(binary_string), 8):
    byte_str = binary_string[i:i+8]
    if len(byte_str) == 8:
        byte_val = int(byte_str, 2)
        bytes_list.append(byte_val ^ 0x67)

with open('out.elf', 'wb') as f:
    f.write(bytes(bytes_list))

print("Done")
