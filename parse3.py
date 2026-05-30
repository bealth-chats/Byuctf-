import re

def parse():
    with open('asm.txt', 'r') as f:
        lines = f.readlines()

    main_start = False

    blocks = {}
    current_block_id = None
    addr_to_block = {}

    # regexes
    re_mov_id = re.compile(r'\s+([0-9a-f]+):\s+be ([0-9a-f]{2} ){1,3}00 00\s+mov\s+\$0x([0-9a-f]+),%esi')

    for line in lines:
        if "<main>:" in line:
            main_start = True
            current_block_id = 0
            addr_to_block['1317'] = 0
            blocks[0] = {'addr': '1317', 'edges': []}
            continue

        if not main_start:
            continue
        if "<_fini>:" in line:
            break

        # extract mov block id
        # it can be:
        # be 00 00 00 00 (mov $0, %esi)
        # be 70 02 00 00 (mov $0x270, %esi)
        # be 02 00 00 00 (mov $2, %esi)
        if "mov" in line and "%esi" in line and "be " in line:
            parts = line.split("mov")
            addr_part = line.split(":")[0].strip()
            # extract hex value after $0x
            if "$0x" in parts[1]:
                val_str = parts[1].split("$0x")[1].split(",")[0]
                block_id = int(val_str, 16)
                addr_to_block[addr_part] = block_id
                blocks[block_id] = {'addr': addr_part, 'edges': []}

    print(f"Mapped {len(blocks)} blocks")

    # second pass
    current_block_id = 0
    current_val = None

    for line in lines:
        if "<main>:" in line:
            main_start = True
            current_block_id = 0
            continue

        if not main_start:
            continue
        if "<_fini>:" in line:
            break

        if "mov" in line and "%esi" in line and "be " in line:
            parts = line.split("mov")
            if "$0x" in parts[1]:
                val_str = parts[1].split("$0x")[1].split(",")[0]
                current_block_id = int(val_str, 16)
            continue

        if "cmpl" in line and "-0x4(%rbp)" in line:
            parts = line.split("cmpl")
            val_str = parts[1].split("$0x")[1].split(",")[0]
            current_val = int(val_str, 16)
            continue

        if "jmp" in line and current_val is not None:
            # e9 11 59 00 00       	jmp    6c68 <main+0x5951>
            addr_target = line.split("jmp")[1].strip().split(" ")[0]
            blocks[current_block_id]['edges'].append((current_val, addr_target))
            current_val = None
            continue

        if "je " in line and current_val is not None:
            # 0f 84 31 1e 00 00    	je     3192 <main+0x1e7b>
            # OR 74 05             je     1234
            addr_target = line.split("je")[1].strip().split(" ")[0]
            blocks[current_block_id]['edges'].append((current_val, addr_target))
            current_val = None
            continue

    for block_id, data in blocks.items():
        new_edges = []
        for val, target_addr in data['edges']:
            target_block_id = None

            # Find closest block start
            closest = -1
            for addr, b_id in addr_to_block.items():
                if int(addr, 16) <= int(target_addr, 16) and int(addr, 16) > closest:
                    closest = int(addr, 16)
                    target_block_id = b_id

            if target_block_id is not None:
                new_edges.append((val, target_block_id))

        blocks[block_id]['edges'] = new_edges

    print(f"Target block 0x270 (624) exists: {0x270 in blocks}")

    queue = [(0, [])]
    visited = set([0])

    while queue:
        curr, path = queue.pop(0)

        if curr == 0x270:
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
