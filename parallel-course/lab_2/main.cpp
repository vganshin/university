#include <iostream>
#include <mpi.h>
#include <fstream>

using namespace std;

#define ROOT 0

int proc_rank;
int proc_num;

struct Matrix {
    int n;
    double** a;
    double* b;
};

Matrix init_matrix(int n) {
    double** a = new double*[n];
    double* b = new double[n];


    for (int row = 0; row < n; row++) {
        a[row] = new double[n];
    }

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            a[i][j] = 0;
        }
    }

    for (int i = 0; i < n; i++) {
        b[i] = 0;
    }

    Matrix matrix;

    matrix.n = n;
    matrix.a = a;
    matrix.b = b;

    return matrix;
}

Matrix read_matrix(string filename) {
    ifstream in(filename);

    int n;

    in >> n;

    Matrix matrix = init_matrix(n);

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            in >> matrix.a[i][j];
        }
        in >> matrix.b[i];
    }

    return matrix;
}

// double calc(Matrix matrix, double* x, int k) {
//     double sum = 0;

//     for (int i = 0; i < n; i++) {
//         if (i != k) {
//             sum += matrix.a[k][i] * x[i];
//         }
//     }

//     return (matrix.b[k] - sum) / matrix.a[k][k];
// }

int main(int argc, char* argv[]) {
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc_num);

    Matrix matrix;
    int n;

    int x_len;
    double* x;

    if (proc_rank == ROOT) {
        matrix = read_matrix("in.txt");
        n = matrix.n;

        x = new double[n];

        for (int i = 0; i < n; i++) {
            x[i] = matrix.b[i] / matrix.a[i][i];
        }

        // Проверить на сходимость (в руте)
    }

    // Bcast start
    MPI_Bcast(&n, 1, MPI_INT, ROOT, MPI_COMM_WORLD);

    // x_len = n % p == 0 ? n : (n / p + 1) * p;
    // x = new double[x_len];

    if (proc_rank != ROOT) {
        matrix = init_matrix(n);
        x = new double[n];
    }

    MPI_Bcast(matrix.b, matrix.n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);

    for (int i = 0; i < n; i++) {
        MPI_Bcast(matrix.a[i], n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);
    }

    MPI_Bcast(x, matrix.n, MPI_DOUBLE, ROOT, MPI_COMM_WORLD);

    // Bcast print

    // if (proc_rank != ROOT) {
    //     cout << "pr = " << proc_rank << ", n = " << matrix.n << endl;

    //     for (int i = 0; i < n; i++) {
    //         for (int j = 0; j < n; j++) {
    //             cout << matrix.a[i][j] << " ";
    //         }
    //         cout << "| " << matrix.b[i] << endl;
    //     }

    //     for (int i = 0; i < n; i++) {
    //         cout << x[i] << " ";
    //     }
    //     cout << endl;
    // }

    // Bcast end

    // Посчитать



    double* old_x = x;
    x = new int[n];
    int m = n / proc_num == 0 ? n / proc_num : n / proc_num + 1;
    int gather_len = proc_num * m;
    double* gather_arr = new double[gather_len];

    for (int i = 0; i < m; i++) {
        int j = m * proc_rank + i;
        if (j < n) {

        } else {

        }
    }


    // int MPI_Gather(void* sendbuf, int sendcount, MPI_Datatype sendtype, void* recvbuf, int recvcount, MPI_Datatype recvtype, int root, MPI_Comm comm)


    MPI_Finalize();

    return 0;
}

// int wow(int argc, char* argv[])
// {
//   int errCode, tmp;

//   MPI_Status status;

//   if ((errCode = MPI_Init(&argc, &argv)) != 0)
//   {
//     return errCode;
//   }

//   int myRank;

//   MPI_Comm_rank(MPI_COMM_WORLD, &myRank);

//   if (myRank == 0)
//   {
//     int mpiSize;

//     MPI_Comm_size(MPI_COMM_WORLD, &mpiSize);

//     cout << "Main! " << myRank << " " << mpiSize << endl;

//     for (int i = 1; i < mpiSize; i++) {
//       MPI_Recv(&tmp, 1, MPI_INT, i, 0, MPI_COMM_WORLD, &status);

//       cout << "Получено сообщение от " << i << ": " << tmp << endl;
//     }

//   }
//   else
//   {
//     cout << "Slave " << myRank << endl;

//     tmp = myRank * myRank;

//     MPI_Send(&tmp, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);
//   }

//   MPI_Finalize();
//   return 0;
// }