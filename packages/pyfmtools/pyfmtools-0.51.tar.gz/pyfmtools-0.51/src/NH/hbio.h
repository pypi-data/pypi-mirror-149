#ifndef IOHB_H
#define IOHB_H

#include<stdio.h>
#include<stdlib.h>
#include<sys/types.h>




#ifdef __cplusplus
extern "C" {
#endif

int readHB_info(const char* filename, int* M, int* N, int* nz, char** Type,
                                                      int* Nrhs){return 0;}

int readHB_header(FILE* in_file, char* Title, char* Key, char* Type,
                    int* Nrow, int* Ncol, int* Nnzero, int* Nrhs, int* Nrhsix,
                    char* Ptrfmt, char* Indfmt, char* Valfmt, char* Rhsfmt,
                    int* Ptrcrd, int* Indcrd, int* Valcrd, int* Rhscrd,
                    char *Rhstype){return 0;}

int readHB_mat_double(const char* filename, int colptr[], int rowind[],
                                                                 double val[]) {return 0;}

int readHB_newmat_double(const char* filename, int* M, int* N, int* nonzeros,
                         int** colptr, int** rowind, double** val){return 0;}

int readHB_aux_double(const char* filename, const char AuxType, double b[]){return 0;}

int readHB_newaux_double(const char* filename, const char AuxType, double** b){return 0;}

int writeHB_mat_double(const char* filename, int M, int N,
                        int nz, const int colptr[], const int rowind[],
                        const double val[], int Nrhs, const double rhs[],
                        const double guess[], const double exact[],
                        const char* Title, const char* Key, const char* Type,
                        char* Ptrfmt, char* Indfmt, char* Valfmt, char* Rhsfmt,
                        const char* Rhstype){return 0;}

int readHB_mat_char(const char* filename, int colptr[], int rowind[],
                                           char val[], char* Valfmt){return 0;}

int readHB_newmat_char(const char* filename, int* M, int* N, int* nonzeros, int** colptr,
                          int** rowind, char** val, char** Valfmt){return 0;}

int readHB_aux_char(const char* filename, const char AuxType, char b[]){return 0;}

int readHB_newaux_char(const char* filename, const char AuxType, char** b, char** Rhsfmt){return 0;}

int writeHB_mat_char(const char* filename, int M, int N,
                        int nz, const int colptr[], const int rowind[],
                        const char val[], int Nrhs, const char rhs[],
                        const char guess[], const char exact[],
                        const char* Title, const char* Key, const char* Type,
                        char* Ptrfmt, char* Indfmt, char* Valfmt, char* Rhsfmt,
                        const char* Rhstype){return 0;}

int ParseIfmt(char* fmt, int* perline, int* width){return 0;}

int ParseRfmt(char* fmt, int* perline, int* width, int* prec, int* flag){return 0;}

void IOHBTerminate(char* message);

#ifdef __cplusplus
}
#endif

#endif
