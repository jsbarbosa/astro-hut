*.gif : plot.py *.dat
	python $<

*.dat : a.out initial.csv
	./$<

a.out : box2d.c box2d.h
	gcc box2d.c -g -lm

clean :
	rm -r *.out *.png *.dat
