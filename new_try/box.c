#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include "box.h"

int main(int argc, char const *argv[])
{
    tree2d *tree = createTree(10);
    // node2d *node = malloc(sizeof(node2d))

    int i;
    DOUBLE max = RAND_MAX;

    time_t t;
    srand((unsigned) time(&t));

    for(i = 0; i<tree->levels; i++)
    {
        tree->nodes[i].box1->c1.x = -rand()/max;
        tree->nodes[i].box1->c1.y = rand()/max;
        tree->nodes[i].box1->c2.x = rand()/max;
        tree->nodes[i].box1->c2.y = rand()/max;
        tree->nodes[i].box1->c3.x = -rand()/max;
        tree->nodes[i].box1->c3.y = -rand()/max;
        tree->nodes[i].box1->c4.x = -rand()/max;
        tree->nodes[i].box1->c4.y = rand()/max;
        calculateNode(&(tree->nodes[i]));
    }
    printTree2d(tree);
    freeTree2d(tree);
    return 0;
}

void calculateBox(box2d *box)
{
    box->width = box->c2.x - box->c1.x;
    box->height = box->c1.y - box->c3.y;
    box->center.x = box->c1.x + 0.5*box->width;
    box->center.y = box->c3.y + 0.5*box->height;
}

void calculateNode(node2d *node)
{
    calculateBox(node->box1);
    calculateBox(node->box2);
    calculateBox(node->box3);
    calculateBox(node->box4);
}

void printBox2d(box2d *box)
{
    printf("(%f, %f), (%f, %f), (%f, %f), (%f, %f), (%f, %f)\n",
            box->center.x, box->center.y,
            box->c1.x, box->c1.y,
            box->c2.x, box->c2.y,
            box->c3.x, box->c3.y,
            box->c4.x, box->c4.y);
}

void printNode2d(node2d *node)
{
    box2d *box = malloc(sizeof(box2d));

    printBox2d(node->box1);
    printBox2d(node->box2);
    printBox2d(node->box3);
    printBox2d(node->box4);
}

void printTree2d(tree2d *tree)
{
    int i;
    node2d *node = malloc(sizeof(node2d));

    for(i = 0; i < tree->levels; i++)
    {
        *node = tree->nodes[i];
        printNode2d(node);
    }
}

node2d *createNode(void)
{
    node2d *node = malloc(sizeof(node2d));
    node->box1 = malloc(sizeof(box2d));
    node->box2 = malloc(sizeof(box2d));
    node->box3 = malloc(sizeof(box2d));
    node->box4 = malloc(sizeof(box2d));

    return node;
}

tree2d *createTree(int levels)
{
    int i;

    tree2d *tree = malloc(sizeof(tree2d));
    tree->nodes = malloc(levels*sizeof(node2d));
    tree->levels = levels;

    node2d *node;

    for(i = 0; i<tree->levels; i++)
    {
        node = createNode();
        tree->nodes[i] = *node;
        free(node);
    }

    return tree;
}

void freeNode2d(node2d *node)
{
    free(node->box1);
    free(node->box2);
    free(node->box3);
    free(node->box4);
}

void freeTree2d(tree2d *tree)
{
    int i;
    node2d *node;
    for(i = 0; i<tree->levels; i++)
    {
        freeNode2d(&(tree->nodes[i]));
    }
    free(tree->nodes);
    free(tree);
}
