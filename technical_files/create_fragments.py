import sys 
import pandas as pd
import numpy as np

aminoacids = ['ALA', 'ARG', 'ASN', 'ASP',
              'CYS', 'GLN', 'GLU', 'GLY', 
              'HIS', 'ILE', 'LEU', 'LYS', 
              'MET', 'PHE', 'PRO', 'SER', 
              'THR', 'TRP', 'TYR', 'VAL']

fragment_length = 30

pdb_path = sys.argv[1]
chain = sys.argv[2]
csv_path = sys.argv[3]
sample_name = sys.argv[4]

text = []
lines = []
with open(pdb_path, 'r') as f:
    for line in f:
        if line[:4] == 'ATOM':
            line_lst = line.split()
            if len(line_lst) > 3 and line_lst[3] in aminoacids and line_lst[4] == chain:
                text.append(line)
                lines.append(line[:-1].split())
if len(text) == 0:
    sys.exit(42)
df = pd.DataFrame(lines)
df.loc[:, 5] = df.loc[:, 5]

if csv_path == 'none':
    aa_nums = df.loc[:, 5].unique()
    l = len(aa_nums)
    fragments = pd.DataFrame()
    fragments['starts'] = np.random.randint(0, l-fragment_length, int(l/(fragment_length/2)))
    fragments['ends'] = fragments['starts'] + fragment_length
    fragments_exp = pd.DataFrame()
    fragments_exp['starts'] = [aa_nums[i] for i in fragments['starts']]
    fragments_exp['ends'] = [aa_nums[i] for i in fragments['ends']]
else:
    fragments_exp = pd.read_csv(csv_path,  header=None, names=['starts', 'ends'])

for i in range(len(fragments_exp)):
    text_fragment = []
    start = int(fragments_exp['starts'].loc[i])
    end = int(fragments_exp['ends'].loc[i])
    for line in text:
        aa_num = int(line.split()[5])
        if aa_num >= start and aa_num <= end:
            text_fragment.append(line)
    with open(f'./{sample_name}_results/{start}-{end}_{sample_name}.pdb', 'w') as f:
        f.write(''.join(text_fragment) + 'END')
    
print('fragments created')
