#!/bin/bash

if [ "$#" -lt 2 ] || [ "$#" -gt 3 ]; then
    echo "Usage: pipeline <pdb_path> <chain> [<csv_path>]"
    exit 1
fi

pdb_path=$1
csv_path="none"
chain=$2

if [ ! -e "$pdb_path" ]; then
	echo "Provided .pdb does not exist."
	exit 1
fi

name=$(basename "$pdb_path" .pdb)

dir_path="./${name}_results"
tmalign_output_path="$dir_path/tmalign_output"

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

if [ -n "$3" ]; then
	csv_path=$2
	if [ ! -e "$csv_path" ]; then
		echo "Provided .csv does not exist."
		exit 1
	fi
fi

python3 ./technical_files/create_fragments.py "$1" "$chain" "$csv_path" "$name"

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

cd ..

touch "$dir_path/ids.txt"

for result_path in $(find "$dir_path" -type f -name "*_result"); do
    result_name="${result_path##*/}"
    echo $result_name
    python3 ./technical_files/extract_pdb_ids.py $name $result_name
done

mkdir $tmalign_output_path
mkdir $dir_path/real_structures

for id in $(cat $dir_path/ids.txt); do
    wget -P $dir_path/real_structures "https://files.rcsb.org/download/$id.pdb"
	echo "$dir_path/real_structures/$id.pdb"
    TMalign $1 "$dir_path/real_structures/$id.pdb" -o "$tmalign_output_path/$id"
done

mkdir $dir_path/results

for id in $(cat $dir_path/ids.txt); do
    python3 ./technical_files/process_tmalign_output.py $name $id
done