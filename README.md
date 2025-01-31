# fragmentsearch
Fragmentsearch is a [Foldseek](https://github.com/steineggerlab/foldseek)-based pipeline designed to identify proteins with structural similarity to specific fragments of a given protein structure

## Installation
```bash
git clone https://github.com/KalinkinAleksei/fragmentsearch
cd ./fragmentsearch/technical_files
./install_fragmentsearch.sh
cd ..
```
## Usage

To use the tool you should open fragmensearch directory

### There are two mods in which the tool can work:
**1. Auto mode:** In this mode, the space, occupaed by a given `.pdb` structure, devided randomly into cubic subspaces with a side of 30 angstroms. Than, aminoacid residues, located in each subspace, are extracted and foldseek search is performed for each of them. For that mode you shoud provide only a path to `.pdb`:
```bash
./fragmentsearch.sh <path_to_pdb>
```
**2.Manual mode:** In this mode, you manually assign regions for search with a `.csv` file in which the first column contains starts, the second - ends of fragments, the third - chain in which the fragment is located:
```
start_1,end_1,chain_1
start_2,end_2,chain_2
...
start_n-1,end_n-1,chain_n-1
start_n,end_n,chain_n
```
All asiigned regions will be extracted as a united structure and foldseek search will be performed for it. To run the tool in this mode perform:
```bash
./fragmentsearch.sh <path_to_pdb> <path_to_csv>
```
## Results
As result the tool will create a folder named `name_fragments` where name will be replaced with name of provided `.pdb`. The folder will contain `.pdb` files of fragments and results of foldseek search for aech of them.

## Examples
Fragmentsearch provides `example.pdb` to test the tool:
```bash
#Auto mode:
./fragmentsearch.sh ./technical_files/example.pdb A
#Manual mode:
./fragmentsearch.sh ./technical_files/example.pdb A ./technical_files/example.csv
```