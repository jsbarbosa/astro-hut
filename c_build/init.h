#define DOUBLE double

int N;
DOUBLE M, G, EPSILON, TOLERANCE;
DOUBLE *pos_x, *pos_y, *pos_z, *speed_x, *speed_y, *speed_z;
DOUBLE *acc_x, *acc_y, *acc_z;

int *where(int *n, int *pos, DOUBLE *min_bound, DOUBLE *max_bound);
void init_from_files(const char *pos_name, const char *speed_name);
void init_from_ram(DOUBLE *x, DOUBLE *y, DOUBLE *z, DOUBLE *vx, DOUBLE *vy, DOUBLE *vz);
void init_conditions(int n, DOUBLE m, DOUBLE g, DOUBLE epsilon, DOUBLE tolerance);
