#include <iostream>
#include <mpi.h>
#include <fstream>
#include <math.h>

using namespace std;

#define ROOT 0

int proc_rank;
int proc_num;
double start_time;

int n;
int real_n;
double eps;
double** a;
double* b;
double* x_prev;
double* x;

bool can_use_jakobi() {
    for (int i = 0; i < n; i++) {
        double tmp = 0;
        for (int j = 0; j < n; j++) {
            if (i != j) {
                tmp += a[i][j];
            }
        }

        if (a[i][i] < tmp) {
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

        in >> real_n >> eps;

        n = real_n % proc_num == 0 ? real_n : (real_n / proc_num + 1) * proc_num;

        a = new double*[n];
        for (int i = 0; i < n; i++) {
            a[i] = new double[n];
        }
        b = new double[n];
        x_prev = new double[n];

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                a[i][j] = 0;
            }
            b[i] = 0;
        }

        for (int i = 0; i < real_n; i++) {
            for (int j = 0; j < real_n; j++) {
                in >> a[i][j];
            }
            in >> b[i];
        }

        if (!can_use_jakobi()) {
            cout << "Ops..." << endl;
            return 1;
        }

        for (int i = 0; i < n; i++) {
            x_prev[i] = b[i] / a[i][i];
        }
    }

    if (proc_rank == ROOT) {
        start_time = MPI_Wtime();
    }

    MPI_Bcast(&real_n, 1, MPI_INT, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(&n, 1, MPI_INT, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(&eps, 1, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);

    if (proc_rank != ROOT) {
        a = new double*[n];
        for (int i = 0; i < n; i++) {
            a[i] = new double[n];
        }
        b = new double[n];
        x_prev = new double[n];
    }

    for (int i = 0; i < n; i++) {
        MPI_Bcast(a[i], n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
    }
    MPI_Bcast(b, n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(x_prev, n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);

    int k = n / proc_num;
    double max_norm;
    double norm ;
    double tmp;
    x = new double[k];

    do {
        for (int _i = 0; _i < k; _i++) {
            int i = proc_rank * k + _i;

            if (i >= real_n) {
                break;
            }

            x[_i] = b[i];
            for (int j = 0; j < real_n; j++) {
                if (i != j) {
                    x[_i] -= a[i][j] * x_prev[j];
                }
            }
            x[_i] /= a[i][i];
        }

        norm = 0;
        for (int _i = 0; _i < k; _i++) {
            int i = proc_rank * k + _i;
            tmp = fabs(x_prev[i] - x[_i]);
            if (tmp > norm) {
                norm = tmp;
            }
        }

        MPI_Reduce(&norm, &max_norm, 1, MPI_DOUBLE, MPI_MAX, ROOT, MPI_COMM_WORLD);
        MPI_Bcast(&max_norm, 1, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
        MPI_Allgather(x, k, MPI_DOUBLE, x_prev, k, MPI_DOUBLE, MPI_COMM_WORLD);
    } while (max_norm > eps);

    if (proc_rank == ROOT) {
        cout << "time: " << MPI_Wtime() - start_time << " s." << endl;
    }

    if (proc_rank == ROOT) {
        ofstream out("out.txt");

        for (int i = 0; i < real_n; i++) {
            out << x_prev[i] << " ";
        }
        out << endl;
    }

    MPI_Finalize();

    return 0;
}
