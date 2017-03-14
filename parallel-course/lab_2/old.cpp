#include <libiomp/omp.h>
#include <fstream>
#include <iostream>
#include <string>
#include <stdio.h>
#include <unistd.h>
#include <ctime>

using namespace std;



void print_matrix(int_matrix matrix) {
    ofstream out("c.txt");

    out << matrix.row_count << " " << matrix.column_count << endl;

    for (int i = 0; i < matrix.row_count; i++) {
        for (int j = 0; j < matrix.column_count; j++) {
            out << matrix.data[i][j] << " ";
        }
        out << endl;
    }
}

int main() {
    int_matrix a_matrix = read_matrix("a.txt");
    int_matrix b_matrix = read_matrix("b.txt");

    if (a_matrix.column_count != b_matrix.row_count) {
        cout << "wtf?\n";

        return 1;
    }

    int mult_count = a_matrix.column_count;

    int_matrix c_matrix = init_matrix(a_matrix.row_count, b_matrix.column_count);

    double start_time = omp_get_wtime();

    #pragma omp parallel for
    for (int row_column = 0; row_column < c_matrix.row_count * c_matrix.column_count; row_column++) {
        int row = row_column / c_matrix.column_count;
        int column = row_column % c_matrix.column_count;

        for (int mult_iter = 0; mult_iter < mult_count; mult_iter++) {
            c_matrix.data[row][column] += a_matrix.data[row][mult_iter] * b_matrix.data[mult_iter][column];
        }
    }

    cout << "time = " << omp_get_wtime() - start_time << endl;

    print_matrix(c_matrix);

    return 0;
}
