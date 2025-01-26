#!/bin/bash

wget https://mmseqs.com/foldseek/foldseek-linux-avx2.tar.gz
tar xvzf foldseek-linux-avx2.tar.gz
rm -f foldseek-linux-avx2.tar.gz
foldseek databases PDB pdb tmp 
pip install numpy pandas