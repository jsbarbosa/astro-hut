#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "init.h"
#include "box.h"
#include "bruteforce.h"
#include "omp.h"

int main(int argc, char **argv)
{
    /*
    If executed directly
    */
    init_conditions(1000, 2.0, 44.97, 0.02, 1);
    init_from_files("pos_init.txt", "speed_init.txt");
    solver(0, 0.2, 0.05, "Data/");
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

    box *tree = malloc(sizeof(box));

    while(t0 < tmax)
    {
        sprintf(buff_pos, "%s%d_instant.dat", dir, cont);
        sprintf(buff_sp, "%s%d_speed.dat", dir,cont);
        FILE *pos = fopen(buff_pos, "w");
        FILE *speeds = fopen(buff_sp, "w");
        if(cont > 0)
        {
            clean_tree(tree);
        }
        tree = init_tree();
        force(tree);

        // Leapfrog
        #pragma omp parallel for
        for(i=0; i<N; i++)
        {
            v_hx[i] = speed_x[i] + 0.5*acc_x[i]*dt;
            v_hy[i] = speed_y[i] + 0.5*acc_y[i]*dt;
            v_hz[i] = speed_z[i] + 0.5*acc_z[i]*dt;
            pos_x[i] += v_hx[i]*dt;
            pos_y[i] += v_hy[i]*dt;
            pos_z[i] += v_hz[i]*dt;
        }
        clean_tree(tree);
        tree = init_tree();
        force(tree);
        #pragma omp parallel for
        for(i=0; i<N; i++)
        {
            speed_x[i] = v_hx[i] + 0.5*acc_x[i]*dt;
            speed_y[i] = v_hy[i] + 0.5*acc_y[i]*dt;
            speed_z[i] = v_hz[i] + 0.5*acc_z[i]*dt;
        }
        for(i=0; i<N; i++)
        {
            fprintf(pos, "%f %f %f\n", pos_x[i], pos_y[i], pos_z[i]);
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

void single_particle_force(int i, box *tree)
{
    if ((pos_x[i] != tree-> center_of_mass[0]) && (pos_y[i] != tree-> center_of_mass[1]) && (pos_z[i] != tree-> center_of_mass[2]))
    {
        int j;
        DOUBLE cs = tree-> coordinate_size, x, y, z, r, theta, mass;
        mass = tree-> mass;

        x = tree-> center_of_mass[0] - pos_x[i];
        y = tree-> center_of_mass[1] - pos_y[i];
        z = tree-> center_of_mass[2] - pos_z[i];
        r = pow(x, 2.0) + pow(y, 2.0) + pow(z, 2.0);
        theta = cs/pow(r, 0.5);
        r += EPSILON;
        if(theta > TOLERANCE)
        {
            if(tree-> number_of_points == 1)
            {
                acc_x[i] += (x/fabs(x))*mass/r;
                acc_y[i] += (y/fabs(y))*mass/r;
                acc_z[i] += (z/fabs(z))*mass/r;
            }
            else
            {
                box sub;
                for(j = 0; j < tree-> number_of_subs; j++)
                {
                    sub = tree->subBoxes[j];
                    single_particle_force(i, &sub);
                }
            }
        }
        else
        {
            acc_x[i] += (x/fabs(x))*mass/r;
            acc_y[i] += (y/fabs(y))*mass/r;
            acc_z[i] += (z/fabs(z))*mass/r;
        }
    }
}

void force(box *tree)
{
    int i;
    // DOUBLE x, y, z, r, *a;
    #pragma omp parallel for
    for(i=0; i<N; i++)
    {
        acc_x[i] = 0;
        acc_y[i] = 0;
        acc_z[i] = 0;
        single_particle_force(i, tree);
        acc_x[i] *= G;
        acc_y[i] *= G;
        acc_z[i] *= G;
    }
}
