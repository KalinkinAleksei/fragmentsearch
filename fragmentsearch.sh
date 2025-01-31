#!/bin/bash

if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
    echo "Usage: pipeline <pdb_path> [<csv_path>]"
    exit 1
fi

pdb_path=$1
csv_path="none"

if [ ! -e "$pdb_path" ]; then
	echo "Provided .pdb does not exist."
	exit 1
fi

name=$(basename "$pdb_path" .pdb)

dir_path="./${name}_results"

if [ -e "$dir_path" ]; then
	echo "The $dir_path directory already exists"
	echo 'Press "Enter" if You want to rewrite the directory'
	echo 'Type "n" to exit the programm'
	read -p "Type Your answer: " user_choice

	if [[ "$user_choice" == "" ]]; then
        echo "Rewriting $dir_path directory"
		rm -rf $dir_path
    else
        echo "Exiting prodram..."
        exit 1
    fi
fi

mkdir $dir_path

if [ -n "$2" ]; then
	csv_path=$2
	if [ ! -e "$csv_path" ]; then
		echo "Provided .csv does not exist."
		exit 1
	fi
fi

python3 ./technical_files/create_fragments.py "$1" "$csv_path" "$name"

if [ $? -eq 42 ]; then
    echo "Chain $chain does not present in $pdb_path"
    exit 1
fi

cd $dir_path

for pdb_file in "."/*.pdb; do
	base_name=$(basename "$pdb_file" .pdb)
	echo "$pdb_file"
	../technical_files/foldseek/bin/foldseek easy-search "$pdb_file" ../technical_files/pdb "${base_name}_result" tmp
done

rm -rf tmp
