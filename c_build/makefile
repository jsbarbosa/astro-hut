run : 1_instant.dat
	python animate.py

1_instant.dat : a.out
	./a.out
	
a.out : bruteforce.c
	gcc -lm bruteforce.c

clean :
	rm -f a.out *.dat
