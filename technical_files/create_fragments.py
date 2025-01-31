import sys 
import pandas as pd
import numpy as np

aminoacids = ['ALA', 'ARG', 'ASN', 'ASP',
              'CYS', 'GLN', 'GLU', 'GLY', 
              'HIS', 'ILE', 'LEU', 'LYS', 
              'MET', 'PHE', 'PRO', 'SER', 
              'THR', 'TRP', 'TYR', 'VAL']

pdb_path = sys.argv[1]
csv_path = sys.argv[2]
sample_name = sys.argv[3]

text = []
lines = []
with open(pdb_path, 'r') as f:
    for line in f:
        if line[:4] == 'ATOM':
            line_lst = line.split()
            if line_lst[3] in aminoacids:
                text.append(line)
                lines.append(line[:-1].split())

df = pd.DataFrame(lines)

if csv_path == 'none':
    for i in [6, 7, 8]:
        df.loc[:, i] = df.loc[:, i].apply(float)

    max_x = df.loc[:, 6].max()
    min_x = df.loc[:, 6].min()
    max_y = df.loc[:, 7].max()
    min_y = df.loc[:, 7].min()
    max_z = df.loc[:, 8].max()
    min_z = df.loc[:, 8].min()

    def define_limits(max_val, min_val, selection_edge_size):
        return max_val - selection_edge_size/2, min_val + selection_edge_size/2

    selection_edge_size = 30
    boarders = [define_limits(max_x, min_x, selection_edge_size),
              define_limits(max_y, min_y, selection_edge_size),
              define_limits(max_z, min_z, selection_edge_size)]

    def culck_dist(max_val, min_val):
        if min_val*max_val > 0:
            dist = abs(abs(max_val) - abs(min_val))
        else:
            dist = abs(max_val) + abs(min_val)
        return dist

    x_edge = culck_dist(max_x, min_x)
    y_edge = culck_dist(max_y, min_y)
    z_edge = culck_dist(max_z, min_z)
    V = x_edge*y_edge*z_edge
    ratio = V/(selection_edge_size**3)
    n = int(ratio)
    for i in range(n):
        coordinates = [np.random.uniform(low, high) for low, high in boarders]
        x_lim = [coordinates[0] - selection_edge_size/2, coordinates[0] + selection_edge_size/2]
        y_lim = [coordinates[1] - selection_edge_size/2, coordinates[1] + selection_edge_size/2]
        z_lim = [coordinates[2] - selection_edge_size/2, coordinates[2] + selection_edge_size/2]
        selected_aminoacids = []
        for i in range(len(df)):
            X = df.loc[i, 6] > x_lim[0] and df.loc[i, 6] <  x_lim[1]
            Y = df.loc[i, 7] > y_lim[0] and df.loc[i, 7] <  y_lim[1]
            Z = df.loc[i, 8] > z_lim[0] and df.loc[i, 8] <  z_lim[1]
            if X and Y and Z:
                res_num = df.loc[i, 5]
                if res_num not in selected_aminoacids:
                    selected_aminoacids.append(str(res_num))
        if len(selected_aminoacids) > 25:
            selection = []
            for i in range(len(lines)):
                if lines[i][5] in selected_aminoacids:
                    selection.append(i)
            def create_coor_name(coor):
                coor = round(coor, 2)
                if coor < 0:
                    return 'm'+str(coor)
                return str(coor)
            x = create_coor_name(coordinates[0])
            y = create_coor_name(coordinates[1])
            z = create_coor_name(coordinates[2])
            with open(f'./{sample_name}_results/{x}_{y}_{z}_{sample_name}.pdb', 'w') as f:
                f.write(''.join([text[i] for i in selection]))
else:
    fragments_exp = pd.read_csv(csv_path,  header=None, names=['start', 'end', 'chain'])
    text_fragment = []
    for i in range(len(fragments_exp)):
        start = int(fragments_exp['start'].loc[i])
        end = int(fragments_exp['end'].loc[i])
        chain = fragments_exp['chain'].loc[i]
        for line in text:
            aa_num = int(line.split()[5])
            aa_chain = line.split()[4]
            if aa_num >= start and aa_num <= end and aa_chain == chain:
                text_fragment.append(line)
    with open(f'./{sample_name}_results/{sample_name}_fragment.pdb', 'w') as f:
        f.write(''.join(text_fragment) + 'END')
print('fragments created')
