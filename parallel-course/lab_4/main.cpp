#include <libiomp/omp.h>
#include <fstream>
#include <iostream>
#include <climits>

using namespace std;

int main() {
    int vertex_num, edge_num;

    ifstream in("in.txt");

    in >> vertex_num >> edge_num;

    int** edges = new int*[vertex_num];

    for (int i = 0; i < vertex_num; i++) {
        edges[i] = new int[vertex_num];
    }

    for (int i = 0; i < vertex_num; i++) {
        for (int j = 0; j < vertex_num; j++) {
            edges[i][j] = INT_MAX;
        }
    }

    int from, to, weight;
    for (int i = 0; i < edge_num; i++) {
        in >> from >> to >> weight;

        edges[from][to] = weight;
        edges[to][from] = weight;
    }

    double start_time, parallel_time, seq_time;
    int num_of_threads = omp_get_max_threads();
    int* min_destinations = new int[num_of_threads];
    int* min_indexes = new int[num_of_threads];
    int min_destination;
    int min_index;


    int visited_count = 0;
    bool* visited = new bool[vertex_num];
    for (int i = 0; i < vertex_num; i++) {
        visited[i] = false;
    }


    int* destinations = new int[vertex_num];
    for (int i = 0; i < vertex_num; i++) {
        destinations[i] = INT_MAX;
    }
    destinations[0] = 0;


    double common_start_time = omp_get_wtime();
    while (visited_count < vertex_num) {
        start_time = omp_get_wtime();
        for (int i = 0; i < num_of_threads; i++) {
            min_destinations[i] = INT_MAX;
        }

        #pragma omp parallel for
        for (int i = 0; i < vertex_num; i++) {
            int thread_num = omp_get_thread_num();
            if (!visited[i] && destinations[i] < min_destinations[thread_num]) {
                min_destinations[thread_num] = destinations[i];
                min_indexes[thread_num] = i;
            }
        }

        min_destination = INT_MAX;

        for (int i = 0; i < num_of_threads; i++) {
            if (min_destinations[i] < min_destination) {
                min_destination = min_destinations[i];
                min_index = min_indexes[i];
            }
        }

        if (min_destination == INT_MAX) {
            break;
        }

        visited[min_index] = true;
        visited_count++;
        seq_time += omp_get_wtime() - start_time;


        start_time = omp_get_wtime();
        #pragma omp parallel for private(weight)
        for (int i = 0; i < vertex_num; i++) {
            if (visited[i]) {
                continue;
            }

            weight = edges[min_index][i];
            if (weight == INT_MAX) {
                continue;
            }

            int tmp = destinations[min_index] + weight;
            if (tmp < destinations[i]) {
                destinations[i] = tmp;
            }
        }
        parallel_time += omp_get_wtime() - start_time;
    };

    cout << "total: " << omp_get_wtime() - common_start_time << " s." << endl;
    cout << "  sum: " << seq_time + parallel_time << " s.";
    cout << " (" << seq_time << " + " << parallel_time << ")" << endl;

    for (int i = 0; i < vertex_num; i++) {
        if (destinations[i] == INT_MAX) {
            cout << "INF";
        }
        else {
            cout << destinations[i];
        }
        cout << " ";
    }
    cout << endl;

    for (int i = 0; i < vertex_num; i++) {
        delete[] edges[i];
    }
    delete[] edges;
    delete[] min_destinations;
    delete[] min_indexes;
    delete[] visited;
    delete[] destinations;

    return 0;
}
