import sys

name = sys.argv[1]
id = sys.argv[2]

lines = []
with open(f'./{name}_results/tmalign_output/{id}', 'r') as f:
    for line in f.readlines():
        if line[:4] == 'ATOM':
            if line.split()[4] == 'A':
                lines.append(line)

with open(f'./{name}_results/results/{id}_common.pdb', 'w') as f:
    f.write(''.join(lines))