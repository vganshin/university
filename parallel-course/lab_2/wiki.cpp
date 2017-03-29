#include <math.h>
#include <iostream>
#include <fstream>
const double eps = 0.001; ///< желаемая точность

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
	} while (norm > eps);
	delete[] TempX;
}

int main(int argc, char* argv[]) {
	ifstream in("in.txt");

    in >> n;

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
        x[i] = -1000.; //b[i] / a[i][i];
    }

    jacobi(n, a, b, x);


    for (int i = 0; i < n; i++) {
    	cout << x[i] << endl;
    }

	return 0;
}