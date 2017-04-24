#include "init.h"
#include <stdio.h>
#include <stdlib.h>

void init_conditions(int n, DOUBLE m, DOUBLE g, DOUBLE epsilon, DOUBLE tolerance)
{
    N = n;
    M = m;
    G = g;
    EPSILON = epsilon;
    TOLERANCE = tolerance;
}

void init_from_ram(DOUBLE *x, DOUBLE *y, DOUBLE *z, DOUBLE *vx, DOUBLE *vy, DOUBLE *vz)
{
    pos_x = malloc(N*sizeof(DOUBLE));
    pos_y = malloc(N*sizeof(DOUBLE));
    pos_z = malloc(N*sizeof(DOUBLE));
    speed_x = malloc(N*sizeof(DOUBLE));
    speed_y = malloc(N*sizeof(DOUBLE));
    speed_z = malloc(N*sizeof(DOUBLE));
    acc_x = malloc(N*sizeof(DOUBLE));
    acc_y = malloc(N*sizeof(DOUBLE));
    acc_z = malloc(N*sizeof(DOUBLE));

    int i = 0;
    for(i = 0; i < N; i++)
    {
        pos_x[i] = x[i];
        pos_y[i] = y[i];
        pos_z[i] = z[i];
        speed_x[i] = vx[i];
        speed_y[i] = vy[i];
        speed_z[i] = vz[i];
    }
}

void init_from_files(const char *pos_name, const char *speed_name)
{
    /*
     * DEPRECATED
     * Use init_from_ram
     */
    int i=0;
    // DOUBLE x, y, z;
    pos_x = malloc(N*sizeof(DOUBLE));
    pos_y = malloc(N*sizeof(DOUBLE));
    pos_z = malloc(N*sizeof(DOUBLE));
    speed_x = malloc(N*sizeof(DOUBLE));
    speed_y = malloc(N*sizeof(DOUBLE));
    speed_z = malloc(N*sizeof(DOUBLE));
    acc_x = malloc(N*sizeof(DOUBLE));
    acc_y = malloc(N*sizeof(DOUBLE));
    acc_z = malloc(N*sizeof(DOUBLE));

    FILE *pos = fopen(pos_name, "r");
    FILE *speeds = fopen(speed_name, "r");
    char line[256];

    while(fgets(line, sizeof(line), pos))
    {
        sscanf(line, "%lf %lf %lf\n", &pos_x[i], &pos_y[i], &pos_z[i]);
        i ++;
    }
    i = 0;
    while(fgets(line, sizeof(line), speeds))
    {
        sscanf(line, "%lf %lf %lf\n", &speed_x[i], &speed_y[i], &speed_z[i]);
        i ++;
    }
    fclose(pos);
    fclose(speeds);
}

int *where(int *n, int *pos, DOUBLE *min_bound, DOUBLE *max_bound)
{
    int i = 0, j = 0;
    DOUBLE x, y, z;
    int *the_ones = malloc(*n*sizeof(int));

    for(i = 0; i<*n; i++)
    {
        x = pos_x[pos[i]];
        y = pos_y[pos[i]];
        z = pos_z[pos[i]];
        if((x >= min_bound[0]) && (x < max_bound[0]))
        {
            if((y >= min_bound[1]) && (y < max_bound[1]))
            {
                if((z >= min_bound[2]) && (z < max_bound[2]))
                {
                    the_ones[j] = pos[i];
                    j++;
                }
            }
        }
    }
    the_ones = realloc(the_ones, j*sizeof(int));
    *n = j;
    return the_ones;
}