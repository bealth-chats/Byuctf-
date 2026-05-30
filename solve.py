import re
import sys

def parse():
    with open('asm.txt', 'r') as f:
        lines = f.readlines()

    main_start = False

    blocks = {}
    current_block_id = None

    # We need to map address to block ID
    addr_to_block = {}

    for line in lines:
        if "<main>:" in line:
            main_start = True
            current_block_id = 0
            addr_to_block['1317'] = 0 # main start
            blocks[0] = {'addr': '1317', 'edges': []}
            continue

        if not main_start:
            continue

        if "<_fini>:" in line:
            break

        # Match `be ... mov $..., %esi` for block ids
        m = re.match(r'\s+([0-9a-f]+):\s+be ([0-9a-f]{2}) ([0-9a-f]{2}) 00 00\s+mov\s+\$0x([0-9a-f]+),%esi', line)
        if not m:
            # Maybe it's single byte: `be XX 00 00 00`
            m = re.match(r'\s+([0-9a-f]+):\s+be ([0-9a-f]{2}) 00 00 00\s+mov\s+\$0x([0-9a-f]+),%esi', line)
            if m:
                addr = m.group(1)
                block_id = int(m.group(3), 16)
                current_block_id = block_id
                addr_to_block[addr] = block_id
                if block_id not in blocks:
                    blocks[block_id] = {'addr': addr, 'edges': []}
                continue
        else:
            addr = m.group(1)
            block_id = int(m.group(4), 16)
            current_block_id = block_id
            addr_to_block[addr] = block_id
            if block_id not in blocks:
                blocks[block_id] = {'addr': addr, 'edges': []}
            continue

    current_block_id = 0
    current_val = None

    re_cmp = re.compile(r'\s+[0-9a-f]+:\s+81 7d fc ([0-9a-f]{2} [0-9a-f]{2} [0-9a-f]{2} [0-9a-f]{2})\s+cmpl\s+\$0x([0-9a-f]+),-0x4\(%rbp\)')
    re_cmp_short = re.compile(r'\s+[0-9a-f]+:\s+83 7d fc ([0-9a-f]{2})\s+cmpl\s+\$0x([0-9a-f]+),-0x4\(%rbp\)')
    re_jmp = re.compile(r'\s+[0-9a-f]+:\s+e9 [0-9a-f]{2} [0-9a-f]{2} [0-9a-f]{2} [0-9a-f]{2}\s+jmp\s+([0-9a-f]+) <.*>')
    re_je = re.compile(r'\s+[0-9a-f]+:\s+0f 84 [0-9a-f]{2} [0-9a-f]{2} [0-9a-f]{2} [0-9a-f]{2}\s+je\s+([0-9a-f]+) <.*>')
    re_je_short = re.compile(r'\s+[0-9a-f]+:\s+74 [0-9a-f]{2}\s+je\s+([0-9a-f]+) <.*>')

    for line in lines:
        if "<main>:" in line:
            main_start = True
            current_block_id = 0
            continue

        if not main_start:
            continue

        if "<_fini>:" in line:
            break

        m = re.match(r'\s+([0-9a-f]+):\s+be ([0-9a-f]{2}) ([0-9a-f]{2}) 00 00\s+mov\s+\$0x([0-9a-f]+),%esi', line)
        if not m:
            m = re.match(r'\s+([0-9a-f]+):\s+be ([0-9a-f]{2}) 00 00 00\s+mov\s+\$0x([0-9a-f]+),%esi', line)
            if m:
                current_block_id = int(m.group(3), 16)
                continue
        else:
            current_block_id = int(m.group(4), 16)
            continue

        # check for comparisons
        m = re_cmp.match(line)
        if m:
            current_val = int(m.group(2), 16)
            continue
        m = re_cmp_short.match(line)
        if m:
            current_val = int(m.group(2), 16)
            continue

        # check for jumps
        m = re_jmp.match(line)
        if m and current_val is not None:
            target_addr = m.group(1)
            blocks[current_block_id]['edges'].append((current_val, target_addr))
            current_val = None
            continue

        m = re_je.match(line)
        if m and current_val is not None:
            target_addr = m.group(1)
            blocks[current_block_id]['edges'].append((current_val, target_addr))
            current_val = None
            continue

        m = re_je_short.match(line)
        if m and current_val is not None:
            target_addr = m.group(1)
            blocks[current_block_id]['edges'].append((current_val, target_addr))
            current_val = None
            continue

    # now map edges back to block IDs
    for block_id, data in blocks.items():
        new_edges = []
        for val, target_addr in data['edges']:
            # Find the closest block start address before the target_addr
            target_block_id = None

            # Let's see if target_addr is in addr_to_block
            if target_addr in addr_to_block:
                target_block_id = addr_to_block[target_addr]
            else:
                # Need to find the closest one
                closest = -1
                for addr, b_id in addr_to_block.items():
                    if int(addr, 16) <= int(target_addr, 16) and int(addr, 16) > closest:
                        closest = int(addr, 16)
                        target_block_id = b_id

            if target_block_id is not None:
                new_edges.append((val, target_block_id))

        blocks[block_id]['edges'] = new_edges

    print(f"Found {len(blocks)} blocks.")

    target_id = 0x270

    if target_id not in blocks:
        print("Target not found in blocks.")
        return

    print("Finding path to block", target_id)

    # bfs
    queue = [(0, [])]
    visited = set([0])

    while queue:
        curr, path = queue.pop(0)

        if curr == target_id:
            print("Found path:", path)
            with open('payload.txt', 'w') as f:
                for p in path:
                    f.write(f"{p}\n")
            return

        if curr not in blocks:
            continue

        for val, nxt in blocks[curr]['edges']:
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [val]))

if __name__ == "__main__":
    parse()
