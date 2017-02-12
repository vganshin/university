#include <iostream>
#include <fstream>
#include <climits>
#include <stdlib.h> /* qsort */

using namespace std;

int *arr, len;

int compare (const void * a, const void * b) {
  return ( *(int*)a - *(int*)b );
}

int main(int argc, char *argv[]) {
    ifstream in("in.txt");

    in >> len;

    arr = new int[len];

    for (int i = 0; i < len; i++) {
        if (i < len) {
            in >> arr[i];
        } else {
            arr[i] = INT_MAX;
        }
    }

    in.close();

    long start_time = clock();

    qsort(arr, len, sizeof(int), compare);

    cout << "time: " << (clock() - start_time) / 1000. << " s" << endl;
}