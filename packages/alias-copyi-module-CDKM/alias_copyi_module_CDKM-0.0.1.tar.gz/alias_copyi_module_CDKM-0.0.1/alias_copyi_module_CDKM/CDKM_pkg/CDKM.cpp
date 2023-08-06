#include "CDKM.h"

CDKM::CDKM(){}

CDKM::CDKM(vector<vector<double>> &X, int c_true, int debug){
    this->N = X.size();
    this->dim = X[0].size();
    this->c_true = c_true;
    this->debug = debug;

    this->X.resize(N, dim);
    for (int i = 0; i < N; i++)
        this->X.row(i) = VectorXd::Map(&X[i][0], X[i].size());

    if (debug == 1){
        cout << "N = " << N << ", dim = " << dim << ", c = " << c_true << endl;
    }
}

CDKM::~CDKM(){}

void CDKM::opt(vector<vector<int>> &init_Y, int ITER){
    Eigen::initParallel();
    int n = Eigen::nbThreads();
    Eigen::setNbThreads(n);

    int rep = init_Y.size();
    Y.resize(rep);
    n_iter_.resize(rep);
    for (int rep_i = 0; rep_i < rep; rep_i++){
        Y[rep_i] = init_Y[rep_i];
        n_iter_[rep_i] = opt_once(Y[rep_i], ITER);
    }

}

int CDKM::opt_once(vector<int> &y, int ITER){

    // xnorm
    VectorXd xnorm(N);
    xnorm = X.rowwise().squaredNorm();

    MatrixXd Sx(dim, c_true);
    VectorXd n(c_true);

    Sx.setZero();
    n.setZero();
    for (int i = 0; i < N; i++){
        Sx.col(y[i]) += X.row(i);
        n(y[i]) += 1;
    }

    VectorXd s(c_true);
    s = Sx.colwise().squaredNorm();


    int iter = 0, c_old = 0, c_new = 0, converge = 0;
    VectorXd delta(c_true);
    VectorXd tmp1(c_true);
    VectorXd tmp2(c_true);
    VectorXd xiSx(c_true);
    std::ptrdiff_t c_new_t;
    int maxOfV;

    for (iter = 0; iter < ITER; iter++){
        converge = 1;
        for (int i = 0; i < N; i++){
            c_old = y[i];
            
            if (n(c_old) == 1){continue;}

            xiSx = X.row(i) * Sx;
            tmp1 = s + 2 * xiSx;
            tmp1.array() += xnorm(i);
            tmp1.array() /= n.array() + 1;
            
            tmp2 = s.array() / n.array();

            delta = tmp1 - tmp2;

            delta(c_old) = s(c_old) / n(c_old) - (s(c_old) - 2 * xiSx(c_old) + xnorm(i)) / (n(c_old) - 1);

            maxOfV = delta.maxCoeff(&c_new_t);
            c_new = (int) c_new_t;

            if (c_new != c_old){
                converge = 0;
                y[i] = c_new;

                Sx.col(c_old) -= X.row(i);
                Sx.col(c_new) += X.row(i);

                s(c_old) = Sx.col(c_old).squaredNorm();
                s(c_new) = Sx.col(c_new).squaredNorm();

                n(c_old) -= 1;
                n(c_new) += 1;
            }

            if (debug && i % 10000 == 0){
                cout << "i = " << i << endl;
            }
        }
        if (debug){
            cout << "iter = " << iter << endl;
        }

        if (converge){
            break;
        }
    }

    if (iter == ITER){
        cout << "not converge" << endl;
    }
    return iter + 1;
}
