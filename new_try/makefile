single_boxes.png : plot.py single_boxes.dat
	python $<

single_boxes.dat : a.out
	./$<

a.out : box2d.c box2d.h
	gcc $< -g

clean :
	rm -r *.out *.png *.dat
