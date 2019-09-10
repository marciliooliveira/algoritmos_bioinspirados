// Simulated Annealing

#include <iostream>
#include <cstdlib>
#include <random>
#include <cmath>
#include <ctime>
#include <fstream>

#define MAX_IT 1000000
#define PI 3.1415

using namespace std;

default_random_engine generator;
normal_distribution<float> distribution(0,0.01);
uniform_real_distribution<double> real_distribution(-1.0,1.0);

int i = 1;

float perturbation(float x) {

    return x + distribution(generator);

}

float test(float x) {

    float nx = pow(2,-2*pow((x-0.1/0.9),2)) * pow(sin(5*PI*x),6);
    return nx;

}

float decreaseG (float dt) {

    return dt * 0.99;

}

float simulated_Annealing() {

    srand(time(0));

    // Temperatura inicial
    float dT = 1500;

    // A definição do X a ser testado deve ser um aleatório qualquer?
    // Ou na faixa de 0 a 1, por exemplo..
    float x = real_distribution(generator);

    float eval = test(x);

    while (i < MAX_IT) {

        float xlin = perturbation(x);
        float xlEval = test(xlin);

        if (xlEval > eval) {
            x = xlin;
            eval = test(x);
        }
        else {
            float aleat = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            float prob = (exp(xlEval - eval)) / dT;

            if (aleat < prob) {
                x = xlin;
                eval = test(x);
            }
        }

        dT = decreaseG(dT);
        i++;

    }

    return eval;

}

int main()
{

    float mediaTempo = 0;
    float mediaIt = 0;
    float mediaConv = 0;
    float porcentTotal = 0;
    ofstream arquivo;
    arquivo.open("metricas.txt");

    arquivo << "Algoritmo Simulated Annealing\n";
    //arquivo << "Amostragem de 35 valores - delta 0.03\n";
    arquivo << "Execução de 10x \n\n";
    arquivo << "Max iteracoes: " << MAX_IT << "\n\n";

    for (int j = 0; j < 10; j++) {
        arquivo << "Numero Rodada: " << j << endl;
        float g = simulated_Annealing();
        mediaIt += i;
        mediaConv += g;
        porcentTotal += g * 100;
        arquivo << "Qtdade Iteracoes: " << i << endl;
        arquivo << "Convergiu para: " << g << endl;
        arquivo << "\n ---------------- \n\n";
    }

    arquivo << "**Media conv " << mediaConv / 10 << endl;
    arquivo << "**Media iter " << mediaIt / 10 << endl;
    arquivo << "**Media % convergencia " << porcentTotal / 10 << endl;

    arquivo.close();

    return 0;
}
