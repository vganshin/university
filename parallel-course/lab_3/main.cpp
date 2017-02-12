#include <iostream>
#include <mpi.h>
#include <fstream>
#include <climits>
#include <stdlib.h> /* qsort */

#define ROOT 0

using namespace std;

int proc_rank;
int proc_num;

MPI_Group world_group;
int *source_arr, *arr;
int source_len, full_len, len, dim;

int compare (const void * a, const void * b) {
  return ( *(int*)a - *(int*)b );
}

void init();
void sort();
void finalize();
int get_dimention();

int main(int argc, char *argv[]) {
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &proc_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc_num);
    MPI_Comm_group(MPI_COMM_WORLD, &world_group);

    init();

    double start_time;
    
    if (proc_rank == ROOT) {
        start_time = MPI_Wtime();
    }

    sort();

    finalize();

    if (proc_rank == ROOT) {
        cout << "time: " << MPI_Wtime() - start_time << " s." << endl;
    }

    MPI_Finalize();
}

void init() {
    if (proc_rank == ROOT) {
        dim = get_dimention();
        
        ifstream in("in.txt");

        in >> source_len;
        full_len = source_len + (source_len % proc_num ? proc_num - source_len % proc_num : 0);

        source_arr = new int[full_len];

        for (int i = 0; i < full_len; i++) {
            if (i < source_len) {
                in >> source_arr[i];
            } else {
                source_arr[i] = INT_MAX;
            }
        }

        in.close();

        len = full_len / proc_num;
    }

    MPI_Bcast(&dim, 1, MPI_INT, ROOT, MPI_COMM_WORLD);
    MPI_Bcast(&len, 1, MPI_INT, ROOT, MPI_COMM_WORLD);

    arr = new int[len];

    MPI_Scatter(source_arr, len, MPI_INT, arr, len, MPI_INT, ROOT, MPI_COMM_WORLD);
}

void sort() {
    qsort(arr, len, sizeof(int), compare);

    MPI_Comm comm;
    int group, pivot;

    for (int i = dim; i > 0; i--) {

        group = proc_rank & (-1 << i);

        MPI_Comm_split(MPI_COMM_WORLD, group, proc_rank, &comm);
        
        int group_rank;

        MPI_Comm_rank(comm, &group_rank);

        if (group_rank == ROOT) {
            pivot = arr[len / 2];
        }

        MPI_Bcast(&pivot, 1, MPI_INT, ROOT, comm);

        int collegue = (group_rank ^ (1 << (i - 1)));

        int pos = 0;
        while (arr[pos] <= pivot && pos < len) {
            pos++;
        }

        int send_len, recv_len, rest_len, *send_arr, *recv_arr, *rest_arr;
        MPI_Status status;

        if (group_rank & (1 << (i - 1))) {
            send_len = pos;
            send_arr = arr;
            rest_len = len - pos;
            rest_arr = arr + pos;
        }
        else {
            send_len = len - pos;
            send_arr = arr + pos;
            rest_len = pos;
            rest_arr = arr;
        }


        MPI_Send(&send_len, 1, MPI_INT, collegue, ROOT, comm);
        MPI_Recv(&recv_len, 1, MPI_INT, collegue, ROOT, comm, &status);

        if (send_len != 0) {
            MPI_Send(send_arr, send_len, MPI_INT, collegue, ROOT, comm);
        }

        recv_arr = new int[recv_len + rest_len];
        if (recv_len != 0) {

            MPI_Recv(recv_arr, recv_len, MPI_INT, collegue, ROOT, comm, &status);
        }
        memcpy(recv_arr + recv_len, rest_arr, rest_len * sizeof(int));

        qsort(recv_arr, recv_len + rest_len, sizeof(int), compare);


        delete[] arr;
        arr = recv_arr;
        len = recv_len + rest_len;
    }
}

void finalize() {
    int *recvcounts = new int[proc_num];
    int *displs = new int[proc_num];

    MPI_Gather(&len, 1, MPI_INT, recvcounts, 1, MPI_INT, ROOT, MPI_COMM_WORLD);

    if (proc_rank == ROOT) {
        displs[0] = 0;
        for (int i = 1; i < proc_num; i++) {
            displs[i] = displs[i - 1] + recvcounts[i - 1];
        }
    }

    MPI_Gatherv(arr, len, MPI_INT, source_arr, recvcounts, displs, MPI_INT, ROOT, MPI_COMM_WORLD);

    // if (proc_rank == ROOT) {
    //     for (int i = 0; i < full_len; i++) {
    //         cout << source_arr[i] << " ";
    //     }
    //     cout << endl;
    // }
}

int get_dimention() {
    int dim = 1;

    while (true) {
        if ((1 << dim) < 0) {
            cout << "proc_num must be 2, 4, 8 or 16 but not " << proc_num << endl;
            exit(1);
        }

        if ((1 << dim) == proc_num) {
            break;
        }

        dim++;
    }

    return dim;
}
