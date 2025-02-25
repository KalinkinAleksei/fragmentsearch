import sys

name = sys.argv[1]
result_name = sys.argv[2]

path = f'./{name}_results'
result_path = f'{path}/{result_name}'
ids = set()

with open(f'{path}/ids.txt', 'r') as f:
    for line in f.readlines():
        ids.add(line)
print(len(ids))

with open(result_path, 'r') as f:
    for line in f.readlines():
        ids.add(line.split()[1][:4])

with open(f'{path}/ids.txt', 'w') as f:
    f.write('\n'.join(ids))