# single_boxes.png : plot.py single_boxes.dat
# 	python $<

single_boxes.dat : a.out initial.csv
	./$<

a.out : box2d.c box2d.h
	gcc box2d.c -g -lm

clean :
	rm -r *.out *.png *.dat
