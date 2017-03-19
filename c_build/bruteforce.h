#define DOUBLE double

void init_from_files(const char *pos_name, const char *speed_name);
void init_from_ram(DOUBLE *x, DOUBLE *y, DOUBLE *z, DOUBLE *vx, DOUBLE *vy, DOUBLE *vz);
void solver(DOUBLE t0, DOUBLE tmax, DOUBLE dt, const char *dir);
void init_conditions(int n, DOUBLE m, DOUBLE g, DOUBLE epsilon, DOUBLE tolerance);
void bounds(DOUBLE *low_bounds, DOUBLE *size);
int *where(int *n, int *pos, DOUBLE *min_bound, DOUBLE *max_bound);


typedef struct box_str
{
    DOUBLE *points;
    DOUBLE *lower_bound;
    DOUBLE *upper_bound;
    DOUBLE *center_of_mass;
    DOUBLE coordinate_size;
    DOUBLE box_half_size;
    DOUBLE mass_unit;
    DOUBLE mass;
    int number_of_subs;
    int number_of_points;
    
    struct box_str *subBoxes;
} box;


box *create_box(int n, int *points,  DOUBLE *lb, DOUBLE cs);
void force(box *tree);
box *init_tree();
void clean_tree(box *tree);
