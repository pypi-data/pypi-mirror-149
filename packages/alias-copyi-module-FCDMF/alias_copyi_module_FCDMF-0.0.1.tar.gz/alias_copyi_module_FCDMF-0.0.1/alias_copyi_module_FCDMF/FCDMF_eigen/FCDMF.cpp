#include "FCDMF.h"

FCDMF::FCDMF(){}

FCDMF::FCDMF(vector<vector<double>> &B, int c_true){
    this->num = B.size();
    this->num_anchor = B[0].size();
    this->c_true = c_true;

    this->B.resize(num, num_anchor);
    for (int i = 0; i < num; i++)
        this->B.row(i) = VectorXd::Map(&B[i][0], B[i].size());


    this->BT.resize(num_anchor, num);
    this->BT = this->B.transpose();

    this->y.resize(num);

    this->P.resize(num, c_true);
    this->P.reserve(num);
    this->Q.resize(num_anchor, c_true);
    this->Q.reserve(num);

    this->S.resize(c_true, c_true);
}

FCDMF::~FCDMF(){}

MatrixXd FCDMF::eudist2_eigen(MatrixXd A, MatrixXd B){
    MatrixXd ret = (-2) * A * B.transpose();
    ret.colwise() += A.rowwise().squaredNorm();
    ret.rowwise() += B.rowwise().squaredNorm().transpose();
    return ret;
}

void FCDMF::opt(int ITER, vector<int> &p0, vector<int> &q0, int a1, int a2){

    vector p = p0;
    vector q = q0;
    spMatXd P = y2Y(p);
    spMatXd Q = y2Y(q);

    int Iter = 0;
    MatXd PTBQ(c_true, c_true);
    MatXd SQT(c_true, num_anchor);
    MatXd STPT(c_true, num);
    MatXd DBP(num, c_true);
    MatXd DBQ(num_anchor, c_true);

    MatXd tmp_cc(c_true, c_true);
    spMatXd PTP(c_true, c_true);
    spMatXd QTQ(c_true, c_true);
    VectorXd vec_c1, vec_c2;
    vector<double> obj(ITER);
    for (Iter = 0; Iter < ITER; Iter++){

        // update S
        PTBQ = P.transpose() * B * Q;
        PTP = P.transpose() * P;
        QTQ = Q.transpose() * Q;
        tmp_cc = PTP.diagonal() * QTQ.diagonal().transpose();
        S = PTBQ.cwiseQuotient(tmp_cc);

        // update p
        SQT = S * Q.transpose();
        DBP = eudist2_eigen(B, SQT);
        update_pq(DBP, p, P, a1);
        P = y2Y(p);

        // update Q
        STPT = S.transpose() * P.transpose();
        DBQ = eudist2_eigen(BT, STPT);
        update_pq(DBQ, q, Q, a2);
        Q = y2Y(q);

        obj[Iter] = compute_obj(B, P, Q, S);
        if (Iter > 2 && (obj[Iter] - obj[Iter - 1])/obj[Iter-1] < 1e-6){
            break;
        }
    }

    for (int i = 0; i < y.size(); i++){
        y[i] = p[i];
    }
}

spMatXd FCDMF::y2Y(vector<int> &y){
    spMatXd Y(y.size(), c_true);
    Y.reserve(y.size());
    for (int i = 0; i < y.size(); i++)
        Y.insert(i, y[i]) = 1;
    
    return Y;
}

void FCDMF::update_pq(MatrixXd &D, vector<int> y, spMatXd Y, int L){
    spMatXd YTY = Y.transpose() * Y;
    VectorXd nc = YTY.diagonal();

    Eigen::Index min_index;
    int c_old, c_new, converge;
    while (2>1){
        converge = 1;
        for (int i = 0; i < Y.rows(); i++){
            c_old = y[i];
            if (nc[c_old] <= L){
                continue;
            }
            auto min_val = D.row(i).minCoeff(&min_index);
            c_new = (int) min_index;

            if (c_new != c_old){
                y[i] = c_new;
                nc[c_old] -= 1;
                nc[c_new] += 1;
                converge = 0;
            }
        }

        if (converge == 1){
            break;
        }
    }
}


double FCDMF::compute_obj(MatXd &B, spMatXd &P, spMatXd &Q, MatXd &S){
    MatXd A = B - P * S * Q.transpose();
    return A.norm();
}

