#include <math.h>
#include <iostream>
#include <fstream>

double eps; ///< желаемая точность
double** a;
double* b;
double* x;
int n;

using namespace std;

/// N - размерность матрицы; A[N][N] - матрица коэффициентов, F[N] - столбец свободных членов,
/// X[N] - начальное приближение, ответ записывается также в X[N];
void jacobi (int N, double** A, double* F, double* X)
{
	double* TempX = new double[N];
	double norm; // норма, определяемая как наибольшая разность компонент столбца иксов соседних итераций.

	do {
		for (int i = 0; i < N; i++) {
			TempX[i] = F[i];
			for (int g = 0; g < N; g++) {
				if (i != g)
					TempX[i] -= A[i][g] * X[g];
			}
			TempX[i] /= A[i][i];
		}
        norm = fabs(X[0] - TempX[0]);
		for (int h = 0; h < N; h++) {
			if (fabs(X[h] - TempX[h]) > norm)
				norm = fabs(X[h] - TempX[h]);
			X[h] = TempX[h];
		}

		// for (int i = 0; i < N; i++) {
		// 	cout << X[i] << " ";
		// }
		// cout << endl;

		// char stop;
		// cin >> stop;
	} while (norm > eps);
	delete[] TempX;
}

int main(int argc, char* argv[]) {
	ifstream in("in.txt");

    in >> n >> eps;

    a = new double*[n];
    for (int i = 0; i < n; i++) {
    	a[i] = new double[n];
    }
    b = new double[n];
    x = new double[n];

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            in >> a[i][j];
        }
        in >> b[i];
    }

    for (int i = 0; i < n; i++) {
        x[i] = b[i] / a[i][i];
    }

    // cout << "a: " << endl;
    // for (int i = 0; i < n; i++) {
    // 	for (int j = 0; j < n; j++) {
    // 		cout << a[i][j] << " ";
    // 	}
    // 	cout << endl;
    // }
    // cout << "b: " << endl;
    // for (int i = 0; i < n; i++) {
    // 	cout << b[i] << " ";
    // }
    // cout << endl;
    // cout << "x: " << endl;
    // for (int i = 0; i < n; i++) {
    // 	cout << x[i] << " ";
    // }
    // cout << endl;

    jacobi(n, a, b, x);


    ofstream out("out.txt");

    for (int i = 0; i < n; i++) {
    	out << x[i] << " ";
    }
    out << endl;

	return 0;
}