#!/bin/bash

for SCHEDULER in "static" "dynamic"; do
	for SIZE in 500 1000; do
		
	python generator.py $SIZE $1 $SIZE

	for THREADS in 1 2 4; do
	for CHUNCK in 1 100 1000; do
		echo "A[$SIZE][$1]×B[$1][$SIZE] OMP_NUM_THREADS=$THREADS OMP_SCHEDULE=$SCHEDULER,$CHUNCK"
		for COUNT in 1 2 3; do
			export OMP_NUM_THREADS=$THREADS
			export OMP_SCHEDULE=$SCHEDULER,$CHUNCK

			g++-6 -fopenmp main.cpp && ./a.out
		done
		echo
	done
	done
	done
done