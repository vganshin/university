#!/bin/bash

mpic++ main.cpp

for N in 2000 1500 1000 500; do
	echo "N = $N"
	python3 generate.py $N 0.001

	for PROCNUM in 4 2 1; do
		echo "proc_num = $PROCNUM"
		for _ in 1 2 3; do
			mpirun -n $PROCNUM a.out
		done
	done
done

python3 generate.py 1000 0.001