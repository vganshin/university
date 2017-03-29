#include <iostream>
#include <mpi.h>
#include <fstream>
#include <math.h>

using namespace std;

#define ROOT 0
#define EPS 0.001

int proc_rank;
int proc_num;

int n;
int real_n;
double* a;
double* b;
double* x_prev;
double* x;

bool can_use_jakobi() {
    for (int i = 0; i < n; i++) {
        double tmp = 0;
        for (int j = 0; j < n; j++) {
            if (i != j) {
                tmp += a[i * n + j];
            }
        }

        if (a[i * n + i] < tmp) {
            return false;
        }
    }

    return true;
}

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc_num);

    if (proc_rank == ROOT) {
        ifstream in("in.txt");

        in >> real_n;

        n = real_n % proc_num == 0 ? real_n : (real_n / proc_num + 1) * proc_num;

        a = new double[n * n];
        b = new double[n];
        x_prev = new double[n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a[i * n + j] = 0;
            }
            b[i] = 0;
        }

        for (int i = 0; i < real_n; i++) {
            for (int j = 0; j < real_n; j++) {
                in >> a[i * n + j];
            }
            in >> b[i];
        }

        if (!can_use_jakobi()) {
            cout << "Ops..." << endl;
            return 1;
        }

        for (int i = 0; i < n; i++) {
            x_prev[i] = b[i] / a[i * n + i];
        }
    }

    MPI_Bcast(&real_n, 1, MPI_INT, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(&n, 1, MPI_INT, ROOT, MPI_COMM_WORLD);

    if (proc_rank != ROOT) {
        a = new double[n * n];
        b = new double[n];
        x_prev = new double[n];
    }

    MPI_Bcast(a, n * n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(b, n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(x_prev, n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);

    int k = n / proc_num;
    double max_norm;
    double norm ;
    double tmp;
    x = new double[k];

    int wow = 0;
    do {
        for (int i = 0; i < k; i++) {
            if (k * proc_rank + i >= real_n) {
                break;
            }

            x[i] = b[proc_rank * k + i];
            for (int j = 0; j < real_n; j++) {
                if ((k * proc_rank + i) != j) {
                    x[i] -= a[(proc_rank * k + i) * n + j] * x_prev[(proc_rank * k + i)];
                }
            }
            x[i] /= a[(proc_rank * k + i) * n + (proc_rank * k + i)];
        }

        norm = 0;
        for (int i = 0; i < k; i++) {
            tmp = fabs(x_prev[k * proc_rank + i] - x[i]);
            if (tmp > norm) {
                norm = tmp;
            }
        }

        MPI_Reduce(&norm, &max_norm, 1, MPI_DOUBLE, MPI_MAX, ROOT, MPI_COMM_WORLD);
        MPI_Bcast(&max_norm, 1, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
        MPI_Allgather(x, k, MPI_DOUBLE, x_prev, k, MPI_DOUBLE, MPI_COMM_WORLD);
        wow++;
    } while (wow < 100000);
    // } while (max_norm > EPS);


    if (proc_rank == ROOT) {

        cout << "max_norm = " << max_norm << endl;
        for (int i = 0; i < n; i++) {
            cout << x_prev[i] << endl;
        }
        // for (int i = 0; i < k; i++) {
        //     cout << x[i] << endl;
        // }
    }

    MPI_Finalize();

    return 0;
}
