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
**1. Auto mode:** In this mode, the given structure is randomly divided into fragments, each consisting of 30 amino acids. For that mode you shoud provide a path to `.pdb` structure and `chain`:
```bash
./fargmentsearch.sh <path to pdb> <chain>
```
**2.Manual mode:** In this mode, you manually assign regions for search with a `.csv` file in which the first column contains starts and the second - ends of fragments:
```
start_1,end_1
start_2,end_2
...
start_n-1,end_n-1
start_n,end_n
```
To run the tool in this mode perform:
```bash
./fargmentsearch.sh <path to pdb> <chain> <path to csv>
```
## Results
As result the tool will create a folder named `name_fragments` where name will be replaced with name of provided `.pdb`. The folder will contain `.pdb` files of fragments and results of foldseek search for aech of them.

## Examples
Fragmentsearch provides `example.pdb` to test the tool:
```bash
#Auto mode:
./fargmentsearch.sh ./technical_files/example.pdb A
#Manual mode:
./fargmentsearch.sh ./technical_files/example.pdb A ./technical_files/example.csv
```