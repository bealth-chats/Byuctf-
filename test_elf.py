with open('pickled.txt', 'r') as f:
    content = f.read().split()

bin_str1 = ''.join(['0' if w == 'rick' else '1' for w in content])
bin_str2 = ''.join(['1' if w == 'rick' else '0' for w in content])

b1 = bytes(int(bin_str1[i:i+8], 2) for i in range(0, len(bin_str1), 8) if len(bin_str1[i:i+8])==8)
b2 = bytes(int(bin_str2[i:i+8], 2) for i in range(0, len(bin_str2), 8) if len(bin_str2[i:i+8])==8)

print("b1 header:", b1[:4])
print("b2 header:", b2[:4])
