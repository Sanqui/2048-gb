DUAL = False

Z80_OPS = """
ldi     eda0
cpi     eda1
ini     eda2
oti     eda3
ldd     eda8
cpd     eda9
ind     edaa
otd     edab
ldir    edb0
cpir    edb1
inir    edb2
otir    edb3
lddr    edb8
cpdr    edb9
indr    edba
otdr    edbb
retn    ed45
"""

z80_ops = {}
for line in Z80_OPS.split('\n'):
    if line:
        instr, op = line.split()
        z80_ops[instr] = int(op, 16)

import sys
for line in sys.stdin.readlines():
    l = line
    line = line.split(';')[0].strip()
    line = line.split()
    if line:
        inst = line[0]
        params = "".join(line[1:])
        params = params.split(',')
        if inst.startswith('!'):
            sys.stdout.write('\t{} {}\n'.format(inst.strip('!'), ", ".join(params)))
        elif inst == 'ld':
            if params[1] == 'a' and params[0] == '[hli]':
                sys.stdout.write('\tld [hl], a\n\tinc hl\n')
            elif params[1] == 'a' and params[0] == '[hld]':
                sys.stdout.write('\tld [hl], a\n\tdec hl\n')
            elif params[0] == 'a' and params[1] == '[hli]':
                sys.stdout.write('\tld a, [hl]\n\tinc hl\n')
            elif params[0] == 'a' and params[1] == '[hld]':
                sys.stdout.write('\tld a, [hl]\n\tdec hl\n')
            elif params[1] == 'sp':
                sys.stderr.write("Err: ld (nnnn), sp\n")
                exit(1)
            elif params[0].startswith('[$ff00+c') and params[1] == 'a':
                sys.stderr.write("Err: ld (ff00+c), a\n")
                exit(1)
            elif params[1] == 'a' and params[0].startswith('[$'):
                addr = int(params[0][2:-1], 16)
                if not DUAL: sys.stdout.write('\tdb ${:x}, ${:x}, ${:x}\n'.format(0x32, addr&0xff, addr>>8))
                else: sys.stdout.write('\tpush hl\n\tld hl, ${:x}\n\tld [hl], a\n\tpop hl\n'.format(addr))
            elif params[1] == 'a' and params[0].startswith('[') and params[0] not in "[hl] [de] [bc]".split():
                label = params[0].strip('[]')
                if not DUAL: sys.stdout.write('\tdb ${:x}\n\tdw {}\n'.format(0x32, label))
                else: sys.stdout.write('\tpush hl\n\tld hl, {}\n\tld [hl], a\n\tpop hl\n'.format(label))
            elif params[0] == 'a' and params[1].startswith('[$'):
                addr = int(params[1][2:-1], 16)
                if not DUAL: sys.stdout.write('\tdb ${:x}, ${:x}, ${:x}\n'.format(0x3a, addr&0xff, addr>>8))
                else: sys.stdout.write('\tpush hl\n\tld hl, ${:x}\n\tld a, [hl]\n\tpop hl\n'.format(addr))
            elif params[0] == 'a' and params[1].startswith('[') and params[1] not in "[hl] [de] [bc]".split():
                label = params[1].strip('[]')
                if not DUAL: sys.stdout.write('\tdb ${:x}\n\tdw {}\n'.format(0x3a, label))
                else: sys.stdout.write('\tpush hl\n\tld hl, {}\n\tld a, [hl]\n\tpop hl\n'.format(label))
            elif params[0] == 'a' and params[1] == 'r':
                sys.stdout.write('\tdb $ed, $5f\n')
            else:
                sys.stdout.write(l)
        elif inst == 'stop':
            sys.stderr.write("Warn: stop\n")
            sys.stdout.write('\thalt\n')
        elif inst == 'reti':
            sys.stdout.write('\tei\n')
            sys.stdout.write('\tret\n')
        elif inst == 'out':
            if params[1] == 'a':
                sys.stdout.write('\tdb $d3,{}\n'.format(params[0].strip('[]')))
            else:
                sys.stdout.write(l)
        elif inst == 'in':
            if params[0] == 'a':
                sys.stdout.write('\tdb $db,{}\n'.format(params[1].strip('[]')))
            else:
                sys.stdout.write(l)
        #elif inst == 'reti':
        elif inst == 'swap':
            sys.stderr.write("Warn: swap\n")
            sys.stdout.write('\trrc a\n'*4)
        elif inst in z80_ops:
            op = z80_ops[inst]
            sys.stdout.write('\tdb ${:x},${:x}\n'.format(op>>8, op&0xff))
        else:
            sys.stdout.write(l)
