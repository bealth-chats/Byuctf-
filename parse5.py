import re

def parse():
    with open('asm.txt', 'r') as f:
        lines = f.readlines()

    main_start = False

    blocks = {}
    current_block_id = None
    addr_to_block = {}

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

        if "mov" in line and "%esi" in line and "be " in line:
            parts = line.split("mov")
            addr_part = line.split(":")[0].strip()
            if "$0x" in parts[1]:
                val_str = parts[1].split("$0x")[1].split(",")[0]
                block_id = int(val_str, 16)
                addr_to_block[addr_part] = block_id
                blocks[block_id] = {'addr': addr_part, 'edges': []}

    print(f"Mapped {len(blocks)} blocks")

    current_block_id = 0
    current_val = None
    last_cmpl_addr = None

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
            last_cmpl_addr = line.split(":")[0].strip()
            continue

        if "jmp" in line:
            if current_val is not None:
                addr_target = line.split("jmp")[1].strip().split(" ")[0]
                # Is it jumping to an address after it? Let's check it manually
                # But notice some jmp are actually jumping back or to next block
                # The jump target can be the literal target!
                blocks[current_block_id]['edges'].append((current_val, addr_target))
                current_val = None
            continue

        if "je " in line:
            if current_val is not None:
                addr_target = line.split("je")[1].strip().split(" ")[0]
                blocks[current_block_id]['edges'].append((current_val, addr_target))
                current_val = None
            continue

    # now map edges back to block IDs
    for block_id, data in blocks.items():
        new_edges = []
        for val, target_addr in data['edges']:
            target_block_id = None

            # Find the target_block_id based on address:
            # We want the block that contains target_addr.
            # A block starts at its mov addr and ends at the next block's mov addr.

            closest_addr = -1
            for addr, b_id in addr_to_block.items():
                addr_int = int(addr, 16)
                t_addr_int = int(target_addr, 16)
                if addr_int <= t_addr_int and addr_int > closest_addr:
                    closest_addr = addr_int
                    target_block_id = b_id

            if target_block_id is not None:
                new_edges.append((val, target_block_id))

        blocks[block_id]['edges'] = new_edges

    print(f"Target block 0x270 (624) exists: {0x270 in blocks}")

    # bfs
    queue = [(0, [])]
    visited = set([0])

    while queue:
        curr, path = queue.pop(0)

        if curr == 0x270:
            print("Found path!", len(path), "steps")
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

    print("Path not found, let's print all reachable nodes from 0")
    print(visited)

if __name__ == "__main__":
    parse()
