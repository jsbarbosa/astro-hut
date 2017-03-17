temp : simulator.py core.c
	rm data/*.dat
	time -f "%e" python simulator.py
core.c : core.pyx setup.py
	python setup.py build_ext --inplace
