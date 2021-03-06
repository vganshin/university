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

    int row, column;

    int_matrix bt = init_matrix(b_matrix.column_count, b_matrix.row_count);

    for(int i = 0; i < bt.row_count; ++i) {
        for(int j = 0; j < bt.column_count; ++j) {
            bt.data[i][j] = b_matrix.data[j][i];
        }
    }

    double start_time = omp_get_wtime();

    #pragma omp parallel for shared(a_matrix, bt, c_matrix) private(row, column)
    for (int row_column = 0; row_column < c_matrix.row_count * c_matrix.column_count; row_column++) {
        row = row_column / c_matrix.column_count;
        column = row_column % c_matrix.column_count;

        for (int mult_iter = 0; mult_iter < mult_count; mult_iter++) {
            c_matrix.data[row][column] += a_matrix.data[row][mult_iter] * bt.data[column][mult_iter];
        }
    }

    cout << "time = " << omp_get_wtime() - start_time << endl;

    print_matrix(c_matrix);

    return 0;
}
