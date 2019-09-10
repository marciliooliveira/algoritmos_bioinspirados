//Hill Climbing estocastico
#include <iostream>
#include <random>
#include <cmath>
#include <time.h>
#include <windows.h>
#include <fstream>

#define MAX_IT 100000
#define PI 3.1415

using namespace std;

default_random_engine g;

normal_distribution<float> distribution(0,0.01);
int i = 0;

float range[11] = {0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0};
/*
float range[101] = {0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09,
                     0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19,
                     0.20, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.29,
                     0.30, 0.31, 0.32, 0.33, 0.34, 0.35, 0.36, 0.37, 0.38, 0.39,
                     0.40, 0.41, 0.42, 0.43, 0.44, 0.45, 0.46, 0.47, 0.48, 0.49,
                     0.50, 0.51, 0.52, 0.53, 0.54, 0.55, 0.56, 0.57, 0.58, 0.59,
                     0.60, 0.61, 0.62, 0.63, 0.64, 0.65, 0.66, 0.67, 0.68, 0.69,
                     0.70, 0.71, 0.72, 0.73, 0.74, 0.75, 0.76, 0.77, 0.78, 0.79,
                     0.80, 0.81, 0.82, 0.83, 0.84, 0.85, 0.86, 0.87, 0.88, 0.89,
                     0.90, 0.91, 0.92, 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99, 1.0};

float range[35] =  {0.0, 0.03, 0.06, 0.09, 0.12, 0.15, 0.18, 0.21, 0.24, 0.27,
                   0.30, 0.33, 0.36, 0.39, 0.42, 0.45, 0.48, 0.51, 0.54, 0.57,
                   0.60, 0.63, 0.66, 0.69, 0.72, 0.75, 0.78, 0.81, 0.84, 0.87,
                   0.90, 0.93, 0.96, 0.99, 1.00};*/

float pertubation(float x) {

    return x + distribution(g);

}

float test(float x) {

    float nx = pow(2,-2*pow((x-0.1/0.9),2)) * pow(sin(5*PI*x),6);
    return nx;

}

float hill_Climbing(float g) {

    srand(time(NULL));

    float x = range[rand()%35];
    float xlin;
    float measured;

    measured = test(x);

    // função maxima de g = 1.0
    for (i=0; i < MAX_IT; i++) {

        if ((measured <= 0.99) || (measured > 1.0)) { // devido a precisão do float!

            xlin = pertubation(x);
            xlin = test(xlin);

            float aleat = static_cast <float> (rand()) / static_cast <float> (RAND_MAX);
            float prob = 1 / (1+exp(measured - xlin)) / 0.001;

            if (aleat < prob) { x = xlin; measured = test(x); }
        }
        else break;

    }

    return measured;

}

int main() {

    float mediaTempo = 0;
    float mediaIt = 0;
    float mediaConv = 0;
    float porcentTotal = 0;
    ofstream arquivo;
    arquivo.open("metricas1.txt");

    arquivo << "Algoritmo Hill Climbing Probabilistico\n";
    arquivo << "Amostragem de 11 valores - delta 0.1\n";
    arquivo << "Execução de 10x \n\n";
    arquivo << "Max iteracoes: " << MAX_IT << "\n\n";

    for (int j = 0; j < 10; j++) {
        arquivo << "Numero Rodada: " << j << endl;
        float ti = GetTickCount();
        float g = hill_Climbing(1.0);
        float tf = GetTickCount();
        mediaTempo += (tf - ti)/1000;
        mediaIt += i;
        mediaConv += g;
        porcentTotal += g * 100;
        arquivo << "Qtdade Iteracoes: " << i << endl;
        arquivo << "Convergiu para: " << g << endl;
        arquivo << "Porcentagem conv: " << g / 100 << endl;
        arquivo << "Tempo Execucao: " << (tf - ti)/1000 << endl;
        arquivo << "\n ---------------- \n\n";
    }

    arquivo << "**Media tempo " << mediaTempo / 10 << endl;
    arquivo << "**Media conv " << mediaConv / 10 << endl;
    arquivo << "**Media iter " << mediaIt / 10 << endl;
    arquivo << "**Media % convergencia " << porcentTotal / 10 << endl;

    arquivo.close();

    return 0;
}
