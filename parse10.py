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
                if block_id == 0x270:
                    addr_to_block['ede4'] = block_id

    print(f"Mapped {len(blocks)} blocks")

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

        if "jmp" in line:
            if current_val is not None:
                addr_target = line.split("jmp")[1].strip().split(" ")[0]
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

            if target_addr in addr_to_block:
                target_block_id = addr_to_block[target_addr]
            else:
                # The compiler might jump to a nop right before the instruction.
                # Let's find the nearest following address in addr_to_block.
                # E.g. block starts at ede5, jump is to ede4 (nop).
                # So we want the SMALLEST address >= target_addr

                # wait, let's look at jump targets.
                t_addr_int = int(target_addr, 16)
                smallest_larger = float('inf')
                for addr, b_id in addr_to_block.items():
                    addr_int = int(addr, 16)
                    # if the block starts exactly at or slightly after the jump target
                    # (since we saw it jumped to a nop)
                    if addr_int >= t_addr_int and addr_int < smallest_larger:
                        # but it shouldn't be too far. say, 16 bytes.
                        if addr_int - t_addr_int <= 16:
                            smallest_larger = addr_int
                            target_block_id = b_id

                if target_block_id is None:
                    # try closest smaller?
                    closest_addr = -1
                    for addr, b_id in addr_to_block.items():
                        addr_int = int(addr, 16)
                        if addr_int <= t_addr_int and addr_int > closest_addr:
                            closest_addr = addr_int
                            target_block_id = b_id

            if target_block_id is not None:
                new_edges.append((val, target_block_id))

        blocks[block_id]['edges'] = new_edges

    # Let's verify that block 0x270 has an incoming edge.
    incoming = []
    for b_id, b_data in blocks.items():
        for val, t_id in b_data['edges']:
            if t_id == 0x270:
                incoming.append((b_id, val))
    print("Incoming to 0x270:", incoming)

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

if __name__ == "__main__":
    parse()
