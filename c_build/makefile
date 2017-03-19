#run : 1_instant.dat
#	python animate.py

1_instant.dat : bruteforce.so core.py test.py
	python test.py
	
bruteforce.so : bruteforce.c bruteforce.h
	gcc -fPIC -shared -O3 -o bruteforce.so bruteforce.c

clean :
	rm -f -r bruteforce.so *.dat __pycache__
