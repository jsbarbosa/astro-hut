#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "bruteforce.h"

int N;
DOUBLE M, G, epsilon;
DOUBLE *pos_x, *pos_y, *pos_z, *speed_x, *speed_y, *speed_z;
DOUBLE *acc_x, *acc_y, *acc_z;

box *create_box(int n, int *points,  DOUBLE *lb, DOUBLE cs, DOUBLE mass);

int main(int argc, char **argv)
{
    init_conditions(1000, 2.0, 44.97, 0.02);
    init_from_files("pos_init.txt", "speed_init.txt");
    temp();
	return 0;
}

void solver(DOUBLE t0, DOUBLE tmax, DOUBLE dt, const char *dir)
{
    int i = 0, cont = 0;
    int number = (tmax - t0)/dt;
    DOUBLE *v_hx = malloc(N*sizeof(DOUBLE));
    DOUBLE *v_hy = malloc(N*sizeof(DOUBLE));
    DOUBLE *v_hz = malloc(N*sizeof(DOUBLE));
    char buff_pos[256];
    char buff_sp[256];
    
    while(t0 < tmax)
    {
        sprintf(buff_pos, "%s%d_instant.dat", dir, cont);
        sprintf(buff_sp, "%s%d_speed.dat", dir,cont);
        FILE *pos = fopen(buff_pos, "w");
        FILE *speeds = fopen(buff_sp, "w");
        force();
        for(i=0; i<N; i++)
        {
            v_hx[i] = speed_x[i] + 0.5*acc_x[i]*dt;
            v_hy[i] = speed_y[i] + 0.5*acc_y[i]*dt;
            v_hz[i] = speed_z[i] + 0.5*acc_z[i]*dt;
            pos_x[i] += v_hx[i]*dt;
            pos_y[i] += v_hy[i]*dt;
            pos_z[i] += v_hz[i]*dt;
            fprintf(pos, "%f %f %f\n", pos_x[i], pos_y[i], pos_z[i]);
        }
        force();
        for(i=0; i<N; i++)
        {
            speed_x[i] = v_hx[i] + 0.5*acc_x[i]*dt;
            speed_y[i] = v_hy[i] + 0.5*acc_y[i]*dt;
            speed_z[i] = v_hz[i] + 0.5*acc_z[i]*dt;
            fprintf(speeds, "%f %f %f\n", speed_x[i], speed_y[i], speed_z[i]);
        }
        t0 += dt;
        if(cont != 0)
        {
            printf("iter: %d of %d\n", cont, number);
        }
        cont += 1;        
        fclose(pos);
        fclose(speeds);
    }
}

void force()
{
    int i, j;
    DOUBLE x, y, z, r;
    for(i=0; i<N; i++)
    {
        for(j=0; j<N; j++)
        {
            if(j == 0)
            {
                acc_x[i] = 0;
                acc_y[i] = 0;
                acc_z[i] = 0;
            }
            if(j!=i)
            {
                x = pos_x[i] - pos_x[j];
                y = pos_y[i] - pos_y[j];
                z = pos_z[i] - pos_z[j];
                r = pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0) + epsilon;
                acc_x[i] += -(x/fabs(x))/r;
                acc_y[i] += -(y/fabs(y))/r;
                acc_z[i] += -(z/fabs(z))/r;
            }
        }
        acc_x[i] *= M*G;
        acc_y[i] *= M*G;
        acc_z[i] *= M*G;
    }
}    

void init_conditions(int n, DOUBLE m, DOUBLE g, DOUBLE e)
{
    N = n;
    M = m;
    G = g;
    epsilon = e;
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

void temp()
{
    int n = N, i;
    int *points = malloc(sizeof(int)*n);
    DOUBLE *low_bounds = malloc(sizeof(DOUBLE)*3);
    box *tree = malloc(sizeof(box));
    DOUBLE rank = 0;
    for(i=0; i<n; i++)
    {
        points[i] = i;
    }
    bounds(low_bounds, &rank);
    tree = create_box(n, points, low_bounds, rank, 1);
}

void bounds(DOUBLE *low_bounds, DOUBLE *size)
{
    int i;
    DOUBLE x_min, x_max, x;
    DOUBLE y_min, y_max, y;
    DOUBLE z_min, z_max, z;
    DOUBLE *rank = malloc(3*sizeof(DOUBLE));
    for(i = 0; i<N; i++)
    {
        if(i == 0)
        {
            x_min = x_max = pos_x[i];
            y_min = y_max = pos_y[i];
            z_min = z_max = pos_z[i];
        }
        x = pos_x[i];
        y = pos_y[i];
        z = pos_z[i];
        if(x < x_min)
        {
            x_min = x;
        }
        else if(x > x_max)
        {
            x_max = x;
        }
        if(y < y_min)
        {
            y_min = y;
        }
        else if(y > y_max)
        {
            y_max = y;
        }
        if(z < z_min)
        {
            z_min = z;
        }
        else if(z > z_max)
        {
            z_max = z;
        }
    }
    
    low_bounds[0] = x_min;
    low_bounds[1] = y_min;
    low_bounds[2] = z_min;
    rank[0] = x_max - x_min;
    rank[1] = y_max - y_min;
    rank[2] = z_max - z_min;
    if ((rank[0] >= rank[1]) && (rank[0] >= rank[2]))
    {
        *size = rank[0];
    }
    else if ((rank[1] >= rank[0]) && (rank[1] >= rank[2]))
    {
        *size = rank[1];
    }
    else if ((rank[2] >= rank[0]) && (rank[2] >= rank[1]))
    {
        *size = rank[2];
    }
    free(rank);
}

DOUBLE *calc_center_of_mass(int n, int *pos)
{
    int i = 0;
    DOUBLE *cm = malloc(3*sizeof(DOUBLE));
    cm[0] = 0; cm[1] = 0; cm[2] = 0;
    for(i = 0; i<n; i++)
    {
        cm[0] += pos_x[pos[i]];
        cm[1] += pos_y[pos[i]];
        cm[2] += pos_z[pos[i]];
    }
    cm[0] *= 1.0/n;
    cm[1] *= 1.0/n;
    cm[2] *= 1.0/n;
    return cm;
}

box *create_box(int n, int *points, DOUBLE *lb, DOUBLE cs, DOUBLE mass)
{
    box *current_box = malloc(sizeof(box));
    current_box-> points = malloc(n*sizeof(DOUBLE));
    current_box-> lower_bound = malloc(3*sizeof(DOUBLE));
    current_box-> upper_bound = malloc(3*sizeof(DOUBLE));
    current_box-> center_of_mass = malloc(3*sizeof(DOUBLE));
    current_box-> coordinate_size = cs;
    current_box-> box_half_size = 0.5*cs;
    current_box-> mass_unit = mass;
    current_box-> mass = mass*n;
    current_box-> number_of_points = n;
    
    DOUBLE *cm = calc_center_of_mass(n, points);
    current_box-> center_of_mass[0] = cm[0];
    current_box-> center_of_mass[1] = cm[1];
    current_box-> center_of_mass[2] = cm[2];
    current_box-> lower_bound[0] = lb[0];
    current_box-> lower_bound[1] = lb[1];
    current_box-> lower_bound[2] = lb[2];
    current_box-> upper_bound[0] = lb[0] + cs;
    current_box-> upper_bound[1] = lb[1] + cs;
    current_box-> upper_bound[2] = lb[2] + cs;
    printf("%f %f %f\n", cm[0], cm[1], cm[2]);
    int i = 0, j, k;
    DOUBLE *min_bound = malloc(3*sizeof(DOUBLE));
    DOUBLE *max_bound = malloc(3*sizeof(DOUBLE));
    int *sub_pos;
    if(n > 1)
    {
        current_box-> subBoxes = malloc(8*sizeof(box));
        k = n;
        min_bound[0] = lb[0];
        min_bound[1] = lb[1];
        min_bound[2] = lb[2];
        max_bound[0] = lb[0] + current_box-> box_half_size;
        max_bound[1] = lb[1] + current_box-> box_half_size;
        max_bound[2] =  lb[2] + current_box-> box_half_size;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[0] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0] + current_box-> box_half_size;
        min_bound[1] = lb[1];
        min_bound[2] = lb[2];
        max_bound[0] = lb[0] + cs;
        max_bound[1] = lb[1] + current_box-> box_half_size;
        max_bound[2] =  lb[2] + current_box-> box_half_size;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[1] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0];
        min_bound[1] = lb[1] + current_box-> box_half_size;
        min_bound[2] = lb[2];
        max_bound[0] = lb[0] + current_box-> box_half_size;
        max_bound[1] = lb[1] + cs;
        max_bound[2] =  lb[2] + current_box-> box_half_size;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[2] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0];
        min_bound[1] = lb[1];
        min_bound[2] = lb[2] + current_box-> box_half_size;
        max_bound[0] = lb[0] + current_box-> box_half_size;
        max_bound[1] = lb[1] + current_box-> box_half_size;
        max_bound[2] =  lb[2] + cs;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[3] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0] + current_box-> box_half_size;
        min_bound[1] = lb[1] + current_box-> box_half_size;
        min_bound[2] = lb[2];
        max_bound[0] = lb[0] + cs;
        max_bound[1] = lb[1] + cs;
        max_bound[2] =  lb[2] + current_box-> box_half_size;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[4] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0] + current_box-> box_half_size;
        min_bound[1] = lb[1];
        min_bound[2] = lb[2] + current_box-> box_half_size;
        max_bound[0] = lb[0] + cs;
        max_bound[1] = lb[1] + current_box-> box_half_size;
        max_bound[2] =  lb[2] + cs;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[5] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0];
        min_bound[1] = lb[1] + current_box-> box_half_size;
        min_bound[2] = lb[2] + current_box-> box_half_size;
        max_bound[0] = lb[0] + current_box-> box_half_size;
        max_bound[1] = lb[1] + cs;
        max_bound[2] =  lb[2] + cs;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[6] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        k = n;
        min_bound[0] = lb[0] + current_box-> box_half_size;
        min_bound[1] = lb[1] + current_box-> box_half_size;
        min_bound[2] = lb[2] + current_box-> box_half_size;
        max_bound[0] = lb[0] + cs;
        max_bound[1] = lb[1] + cs;
        max_bound[2] =  lb[2] + cs;
        sub_pos = where(&k, points, min_bound, max_bound);
        if (k > 0)
        {
            current_box-> subBoxes[6] = *create_box(k, sub_pos, min_bound, current_box-> box_half_size, mass);
        }
        //j += 1;
    }
    //free(sub_pos);
    free(min_bound);
    free(max_bound);
    //printf("%d\n", j);
    return current_box;
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
void init_from_files(const char *pos_name, const char *speed_name)
{
    /*
     * DEPRECATED
     * Use init_from_ram 
     */
    int i=0;
    DOUBLE x, y, z;
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
    char *token;
    
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
