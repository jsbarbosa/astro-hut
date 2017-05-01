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
	return 0;
}

void solver(DOUBLE t0, DOUBLE tmax, DOUBLE dt, const char *dir)
{
    int i = 0, cont = 0;
    int number = (tmax - t0)/dt;
    DOUBLE *v_hx = malloc(N*sizeof(DOUBLE));
    DOUBLE *v_hy = malloc(N*sizeof(DOUBLE));
    DOUBLE *v_hz = malloc(N*sizeof(DOUBLE));


    box *tree = malloc(sizeof(box));

    while(t0 < tmax)
    {
        if(cont > 0)
        {
            clean_tree(tree);
        }
        else
        {
            print_status(dir, 0);
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
            // energy[i] += 0.5*M*(speed_x[i]*speed_x[i]
                                // + speed_y[i]*speed_y[i]
                                // + speed_z[i]*speed_z[i]);
        }
        print_status(dir, cont+1);
        t0 += dt;
        if(cont != 0)
        {
            printf("iter: %d of %d\n", cont, number);
        }
        cont += 1;
    }
}

void single_particle_force(int i, box *tree)
{
    if ((pos_x[i] != tree-> center_of_mass[0]) && (pos_y[i] != tree-> center_of_mass[1]) && (pos_z[i] != tree-> center_of_mass[2]))
    {
        int j;
        DOUBLE cs = tree-> coordinate_size, x, y, z, r, r2, theta, mass;
        mass = tree-> mass;

        x = tree-> center_of_mass[0] - pos_x[i];
        y = tree-> center_of_mass[1] - pos_y[i];
        z = tree-> center_of_mass[2] - pos_z[i];
        r2 = x*x + y*y + z*z;
        r = sqrt(r2);
        theta = cs/r;
        r2 += EPSILON;
        if(theta > TOLERANCE)
        {
            if(tree-> number_of_points == 1)
            {
                acc_x[i] += x*mass/pow(r2, 1.5);
                acc_y[i] += y*mass/pow(r2, 1.5);
                acc_z[i] += z*mass/pow(r2, 1.5);
                // acc_x[i] += (x/fabs(x))*mass/r;
                // acc_y[i] += (y/fabs(y))*mass/r;
                // acc_z[i] += (z/fabs(z))*mass/r;
                // energy[i] += mass/r;
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
            acc_x[i] += x*mass/pow(r2, 1.5);
            acc_y[i] += y*mass/pow(r2, 1.5);
            acc_z[i] += z*mass/pow(r2, 1.5);
            // acc_x[i] += (x/fabs(x))*mass/r2;
            // acc_y[i] += (y/fabs(y))*mass/r2;
            // acc_z[i] += (z/fabs(z))*mass/r2;
            // energy[i] += mass/r;
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
        // energy[i] = 0;
        single_particle_force(i, tree);
        acc_x[i] *= G;
        acc_y[i] *= G;
        acc_z[i] *= G;
        // energy[i] *= 0.5*G*M;
    }
}

void print_status(const char *dir, int contador)
{
    int i;
    char buff_pos[256];
    char buff_sp[256];
    char buff_en[256];

    sprintf(buff_pos, "%s%d_instant.dat", dir, contador);
    sprintf(buff_sp, "%s%d_speed.dat", dir, contador);
    // sprintf(buff_en, "%s%d_energy.dat", dir, contador);
    FILE *pos = fopen(buff_pos, "w");
    FILE *speeds = fopen(buff_sp, "w");
    // FILE *energies = fopen(buff_en, "w");

    for(i=0; i<N; i++)
    {
        fprintf(pos, "%f %f %f\n", pos_x[i], pos_y[i], pos_z[i]);
        fprintf(speeds, "%f %f %f\n", speed_x[i], speed_y[i], speed_z[i]);
        // fprintf(energies, "%f \n", energy[i]);
        
    }
    fclose(pos);
    fclose(speeds);
    // fclose(energies);
}

// void calculateEnergy()
// {
//     int i, j;
//     DOUBLE x, y, z;
//     #pragma omp parallel for private(i, j, x, y, z)
//     for(i = 0; i<N; i++)
//     {
//         kinetic[i] = 0.5*M*(speed_x[i]*speed_x[i]
//                             +speed_y[i]*speed_y[i]
//                             +speed_z[i]*speed_z[i]);
//
//         for(j = 0; j<N; j++)
//         {
//             if(i != j)
//             {
//                 x = pos_x[i] - pos_x[j];
//                 y = pos_y[i] - pos_y[j];
//                 z = pos_z[i] - pos_z[j];
//
//             }
//         }
//
//     }
// }
