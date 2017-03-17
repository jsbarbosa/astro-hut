#include <stdio.h>
#include <stdlib.h>

#define DOUBLE double

void __init__();
void force();
void solver(double t0, double tmax, double dt);

int N=1000;
double m=2.0, G = 44.97, epsilon = 20*0.001;
double *pos_x, *pos_y, *pos_z, *speed_x, *speed_y, *speed_z;
double *acc_x, *acc_y, *acc_z;

int main(int argc, char **argv)
{   
    int i = 0;
    __init__();
    solver(0.0, 2.5, 0.01);
    //for (i = 0; i<N; i++)
    //{
        
        //printf("ax=%f, ay=%f, az=%f\n", acc_x[i], acc_y[i], acc_z[i]);
        ////printf("x=%f, y=%f, z=%f\n", pos_x[i], pos_y[i], pos_z[i]);
        ////printf("vx=%f, vy=%f, vz=%f\n", speed_x[i], speed_y[i], speed_z[i]);
    //}
	return 0;
}

void solver(double t0, double tmax, double dt)
{
    int i = 0, cont = 1;
    double dt2 = pow(dt, 2);//, v_hx, v_hy, v_hz;
    double *v_hx = malloc(N*sizeof(DOUBLE));
    double *v_hy = malloc(N*sizeof(DOUBLE));
    double *v_hz = malloc(N*sizeof(DOUBLE));
    char buff_pos[256];
    char buff_sp[256];
    
    while(t0 < tmax)
    {
        sprintf(buff_pos, "%d_instant.dat", cont);
        printf("%s\n", buff_pos);
        FILE *pos = fopen(buff_pos, "w");
        //FILE *speeds = fopen("0_speed.dat", "r
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
        }
        t0 += dt;
        cont += 1;
        fclose(pos);
    }
}

void force()
{
    int i, j;
    double x, y, z, r;
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
        acc_x[i] *= m*G;
        acc_y[i] *= m*G;
        acc_z[i] *= m*G;
    }
}    

void __init__()
{
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
    
    FILE *pos = fopen("0_instant.dat", "r");
    FILE *speeds = fopen("0_speed.dat", "r");
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
