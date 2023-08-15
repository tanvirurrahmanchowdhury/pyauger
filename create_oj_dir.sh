#!/bin/bash
mkdir -p auger_main
dir=($(find . -type d -name "k_grid_*"))
for d in "${dir[@]}"
do
echo $d
(cd "$d" && cp *npy ../auger_main)
done
