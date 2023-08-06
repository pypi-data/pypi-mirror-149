#ifndef _CDKM_H
#define _CDKM_H

#include <iostream>
#include <algorithm>
#include <fstream>
#include <vector>
#include <numeric>
#include <string>
#include <sstream>
#include "Eigen339/Eigen/Core"

using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;

typedef Eigen::Matrix<double, Eigen::Dynamic, Eigen::Dynamic, Eigen::RowMajor> MatrixXd_Row;

class CDKM{
public:
    int N = 0;
    int dim = 0;
    int c_true = 0;
    int debug = 0;

    vector<int> n_iter_;
    MatrixXd_Row X;
    vector<vector<int>> Y;

    CDKM();
    CDKM(vector<vector<double>> &X, int c_true, int debug);
    ~CDKM();

    void opt(vector<vector<int>> &init_Y, int ITER);
    int opt_once(vector<int> &y, int ITER);
};
#endif //_CDKM_H
