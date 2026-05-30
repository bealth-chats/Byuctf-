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

        if "jne " in line:
            if current_val is not None:
                addr_target = line.split("jne")[1].strip().split(" ")[0]
                # Actually, in cmp/jne/jmp:
                # 1349:	81 7d fc 00 01 00 00 	cmpl   $0x100,-0x4(%rbp)
                # 1350:	75 05                	jne    1357 <main+0x40>
                # 1352:	e9 11 59 00 00       	jmp    6c68 <main+0x5951>
                # The jne target is the NEXT instruction block!
                # The jmp target is the TRUE block!
                pass
            continue

    # now map edges back to block IDs
    for block_id, data in blocks.items():
        new_edges = []
        for val, target_addr in data['edges']:
            target_block_id = None

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

    # Check edges of block 0
    print("Block 0 edges:", blocks[0]['edges'])

    # Check all edges that go to missing nodes...
    all_targets = set()
    for block_id, data in blocks.items():
        for val, target_id in data['edges']:
            all_targets.add(target_id)

    print("Is 624 in targets?", 0x270 in all_targets)

if __name__ == "__main__":
    parse()
