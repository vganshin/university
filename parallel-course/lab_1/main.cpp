#include <libiomp/omp.h>
#include <fstream>
#include <iostream>
#include <string>
#include <stdio.h>
#include <unistd.h> 
#include <ctime>

using namespace std;

struct int_matrix {
    int row_count;
    int column_count;
    int** data;
};

int_matrix init_matrix(int row_count, int column_count) {
    int** data = new int*[row_count];

    for (int row = 0; row < row_count; row++) {
        data[row] = new int[column_count];
    }

    for (int i = 0; i < row_count; i++) {
        for (int j = 0; j < column_count; j++) {
            data[i][j] = 0;
        }
    }

    int_matrix matrix;

    matrix.row_count = row_count;
    matrix.column_count = column_count;
    matrix.data = data;

    return matrix;
}

int_matrix read_matrix(string filename) {
    ifstream in(filename);

    int row_count, column_count;

    in >> row_count >> column_count;

    int_matrix matrix = init_matrix(row_count, column_count);

    int tmp;
    for (int i = 0; i < row_count; i++) {
        for (int j = 0; j < column_count; j++) {
            in >> matrix.data[i][j];
        }
    }

    return matrix;    
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

    return 0;
}
