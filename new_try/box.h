#define DOUBLE float

typedef struct point2d_str
{
    DOUBLE x;
    DOUBLE y;
} point2d;

typedef struct box2d_str
{
    point2d c1;
    point2d c2;
    point2d c3;
    point2d c4;
    DOUBLE width;
    DOUBLE height;
    point2d center;
} box2d;

typedef struct node2d_str
{
    box2d *box1;
    box2d *box2;
    box2d *box3;
    box2d *box4;
    struct node2d_str *child;
} node2d;

typedef struct tree2d_str
{
    node2d *nodes;
    int levels;
} tree2d;

void calculateBox(box2d *box);
void calculateNode(node2d *node);
void printBox2d(box2d *box);
void printNode2d(node2d *node);
void printTree2d(tree2d *tree);
node2d *createNode(void);
tree2d *createTree(int levels);
void freeNode2d(node2d *node);
void freeTree2d(tree2d *tree);
