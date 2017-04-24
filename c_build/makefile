CC = gcc
CC_OPTIONS = -O3 -Wall -fPIC -fopenmp
C_SCRIPTS = init.h box.h bruteforce.h
OBJS = init.o box.o bruteforce.o

EXEC = bruteforce.so
LIBS = -lm

all: $(EXEC)

.c.o:
	$(CC) $(CC_OPTIONS) -c $<

$(EXEC):$(OBJS)
	$(CC) -shared $(LIBS) -o $(EXEC) $(OBJS)
	rm -f $(OBJS)

clean:
	rm -f $(OBJS) *~ ${EXEC}
