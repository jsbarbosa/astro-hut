#run : 1_instant.dat
#	python animate.py

CC = gcc
CC_OPTIONS = -O3 -Wall -fPIC
C_SCRIPTS = init.h box.h bruteforce.h
OBJS = init.o box.o bruteforce.o

EXEC = bruteforce.x
# EXEC = bruteforce.so
LIBS = -lm

all: $(EXEC) #core.py test.py
	python test.py

.c.o:
	$(CC) $(CC_OPTIONS) -c $<

$(EXEC):$(OBJS)
	# $(CC) -shared $(LIBS) -o $(EXEC) $(OBJS)
	$(CC) $(LIBS) -o $(EXEC) $(OBJS)

clean:
	rm -f $(OBJS) *~ core* ${EXEC}
	rm -r __pycache__
