#ifndef FCDMF_H_
#define FCDMF_H_

#include <iostream>
#include <valarray>
#include <chrono>
#include <valarray>
#include <algorithm>
#include <threads.h>
#include "Eigen339/Eigen/Core"
#include "Eigen339/Eigen/Sparse"

using namespace std;

using Eigen::MatrixXd;
using Eigen::VectorXd;

typedef Eigen::SparseMatrix<double, Eigen::ColMajor> spMatXd;
typedef Eigen::SparseMatrix<double, Eigen::RowMajor> spMatXd_Row;

typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::ColMajor> MatXd;
typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> MatXd_Row;

class FCDMF{
public:

    int num;
    int num_anchor;
    int c_true;

    spMatXd P;
    spMatXd Q;

    MatXd B;
    MatXd BT;
    MatXd S;

    vector<int> y;

    FCDMF();
    FCDMF(vector<vector<double>> &B, int c_true);
    ~FCDMF();
    void opt(int ITER, vector<int> &p, vector<int> &q, int a1, int a2);

    MatrixXd eudist2_eigen(MatrixXd A, MatrixXd B);

    spMatXd y2Y(vector<int> &y);
    double compute_obj(MatXd &B, spMatXd &P, spMatXd &Q, MatXd &S);
    void update_pq(MatrixXd &D, vector<int> y, spMatXd Y, int L);

};

#endif
