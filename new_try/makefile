*.gif : plot.py *.dat
	python $<

*.dat : a.out initial.csv
	time ./$<

a.out : box2d.c box2d.h
	gcc box2d.c -lm -O2 -fopenmp -Wall -g

clean :
	rm -r *.out *.png *.dat
