#include <libiomp/omp.h>
#include <fstream>
#include <iostream>
#include <climits>

using namespace std;

struct node {
    int to;
    unsigned int weight;
    struct node* next;
};

node* create_node(int to, int weight, node* next) {
    node* n = (node*) malloc(sizeof(node));

    n->to = to;
    n->weight = weight;
    n->next = next;

    return n;
}

int vertext_num, edge_num;
int* destinations;
bool* visited;
node** edges;

int get_weight(int from, int to) {
    node* current = edges[from];

    while (current != NULL) {
        if (current->to == to) {
            return current->weight;
        }
        current = current->next;
    }

    return INT_MAX;
}

int main() {
    ifstream in("in.txt");

    in >> vertext_num >> edge_num;

    visited = new bool[vertext_num];
    for (int i = 0; i < vertext_num; i++) {
        visited[i] = false;
    }

    destinations = new int[vertext_num];
    for (int i = 0; i < vertext_num; i++) {
        destinations[i] = INT_MAX;
    }
    destinations[0] = 0;

    edges = (node**) malloc(vertext_num * sizeof(node));

    for (int i = 0; i < vertext_num; i++) {
        edges[i] = NULL;
    }

    int from, to, weight;
    for (int i = 0; i < edge_num; i++) {

        in >> from >> to >> weight;

        edges[from] = create_node(to, weight, edges[from]);
        edges[to] = create_node(from, weight, edges[to]);
    }

    node* current;

    int min_d;
    int min_i;

    double start_time, parallel_time, seq_time;

    double common_start_time = omp_get_wtime();

    int visited_count = 0;

    while (visited_count < vertext_num) {
        start_time = omp_get_wtime();
        min_d = INT_MAX;
        for (int i = 0; i < vertext_num; i++) {
            if (!visited[i] && destinations[i] < min_d) {
                min_d = destinations[i];
                min_i = i;
            }
        }

        if (min_d == INT_MAX) {
            break;
        }

        visited[min_i] = true;
        visited_count++;
        seq_time += omp_get_wtime() - start_time;


        start_time = omp_get_wtime();
        #pragma omp parallel for
        for (int i = 0; i < vertext_num; i++) {
            if (!visited[i] && destinations[min_i] + get_weight(min_i, i) > destinations[min_i] && destinations[min_i] + get_weight(min_i, i) < destinations[i]) {
                destinations[i] = destinations[min_i] + get_weight(min_i, i);
            }
        }
        parallel_time += omp_get_wtime() - start_time;
    };

    cout << "total: " << omp_get_wtime() - common_start_time << " s." << endl;
    cout << "  sum: " << seq_time + parallel_time << " s.";
    cout << " (" << seq_time << " + " << parallel_time << ")" << endl;


    return 0;
}
