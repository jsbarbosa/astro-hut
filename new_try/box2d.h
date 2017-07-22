#define DOUBLE float

typedef struct point2d_str
{
    DOUBLE x;
    DOUBLE y;
} point2d;

typedef struct node2d_str
{
    DOUBLE *xs;
    DOUBLE *ys;

    struct node2d_str *subnode1;
    struct node2d_str *subnode2;
    struct node2d_str *subnode3;
    struct node2d_str *subnode4;

    int Nbodies;
    DOUBLE mass;
    DOUBLE width;
    DOUBLE height;
    point2d cmass;
    point2d center;

} node2d;

// GENERAL PURPOSE
point2d *randomPos(int Nbodies);
DOUBLE min(int n, DOUBLE *values);
DOUBLE max(int n, DOUBLE *values);

// PRINTING
void printNode2d(FILE *file, node2d *node);

// BOXES
node2d *calculateNode2d(node2d *mother_node);
node2d *initFirstNode2d(int Nbodies, DOUBLE *xs, DOUBLE *ys);
node2d *createNode2d(int Nbodies, node2d *node, DOUBLE *xs, DOUBLE *ys);
node2d *createSubNode2d(int Nbodies, node2d *node, DOUBLE *xs, DOUBLE *ys, int *pwhere);

// FREEING
void freeNodes2d(node2d *node);
