#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define fm(X,i,j,ld) X[(i)+(j)*(ld)]
#define somalloc(x,n) x = malloc((n)*sizeof(*(x)))
	

extern void dpbtrf_(char *UPLO, int *N, int *KD, double *AB, int *LDAB, int *INFO);	
	
extern void dpbtrs_(char *UPLO, int *N, int *KD, int *NRHS, double *AB, int *LDAB,
	double *B, int *LDB, int *INFO);
		
extern void dsaupd_(int*, const char*, int*, const char*, int*,
    double*, double*, int*, double*, int*, int*, int*, double*,
    double*, int*, int*);

extern void dseupd_(int*, const char*, int*, double*, double*, int*,
    double*, const char*, int*, const char*, int*, double*, double*,
    int*, double*, int*, int*, int*, double*, double*, int*, int*);
		

int main(void)
{
	int m = 300;
	int n = m*m;
	double kappa = 0.000003;
	
	double *AB = malloc((m+1)*n*sizeof(*AB));   //erzeuge bandmatrix AB
	for (int j = 0; j < n; j++){                //erste zeile in AB
		fm(AB, 0, j, m+1) = -1;
	}
	for (int i = 1; i < m-1; i++){
		for (int j = 0; j < n; j++){
			fm(AB,i,j,m+1) = 0;
		}
	}
	for (int j = 0; j < n; j++){      //vorletzte Zeile in AB
		fm(AB, m-1, j, m+1) = -1;
		if (j%m == 0 ){
			fm(AB,m-1,j,m+1) = 0;
		}
	}
            
	for (int j = 0; j < m; j++){    //letzte zeile in AB
		for (int i = 0; i < m; i++){
			fm(AB, m, i+m*j, m+1) = 4 + kappa*(pow((i-m/2),2)+(pow((j-m/2),2)));
		}
	}			
	
	for (int i = 0; i < m+1; i++){         //"linke obere Ecke" von AB muss noch null gesetzt werden.
		for (int j = 0; j < n; j++){
			if (j < m-i){
				fm(AB, i, j, m+1) = 0;
			}	
		}
	}
	/*
	printf("Bandmatrix:\n");            //Bandmatrix AB ausgegeben
	for (int i = 0; i < m+1; ++i){
		for (int j = 0; j < n; ++j){
			printf("%10.3f", AB[i+j*(m+1)]);
		}
		printf("\n");		
	}
	*/
	int ido = 0; // has to be zero on first run
    int info = 0; // has to be zero on first run
    int nev = 17;//5;      //number of eigenvalues; 0 < NEV < N
    double tol = 1e-20;
    double *somalloc(resid, n);  //Double precision array of length N
    int ncv = 2*nev;            //nev < ncv <= n (number of columns of matrix vmat)
    int ldv = n;
    double *somalloc(vmat, ldv*ncv);
    int iparam[11] = {0};
    iparam[1-1] = 1;    // auto shifts
    iparam[3-1] = 10000; // maxiter
    iparam[4-1] = 1;    // has to be 1
    iparam[7-1] = 3;    // mode 3
    int ipntr[11] = {0};
    double *somalloc(workd, 3*n);
    int lworkl =  ncv*ncv + 8*ncv;
    double *somalloc(workl, lworkl);

    int do_arpack = 1;
    double *x = NULL;
    double *y = NULL;
    int niter = 0;
	
	int kd = m;
	int colX = 1;   //the number of columns of the vector X
	int ldAB = m+1;  //The leading dimension of the array AB

	dpbtrf_("U", &n, &kd, AB, &ldAB, &info);
	printf("INFO (nach dpbtrf_): %d\n", info);
	
    do{
        dsaupd_(&ido, "I", &n, "LM", &nev, &tol, resid, &ncv,
            vmat, &ldv, iparam, ipntr, workd, workl, &lworkl, &info);
			
        switch (ido){
            case -1: // fall-through
            case +1: do_arpack = 1; // repeat arpack
                     x = workd + ipntr[1-1]-1;
                     y = workd + ipntr[2-1]-1;
					dpbtrs_("U", &n, &kd, &colX, AB, &ldAB, x, &n, &info);

                     for (int i = 0; i < n; i++)
                     {
						y[i] = x[i];
                     }

                     niter += 1;
                     break;
            case 99: do_arpack = 0; // we are done
                     break;
            default:
                fprintf(stderr, "Should not happen!\n");
                return -1;
        }
    }
    while (do_arpack);
	printf("ido: %d\n", ido);
    printf("Info (nach dsaupd_ und dpbtrs_): %d\n", info);

    int rvec = 1; // 1: compute eigenvectors
    int *somalloc(sel, ncv);
    double *somalloc(eigvals, nev);
    double *somalloc(eigvecs, n*nev);
	double sigma = 0;       //shift = 0 (eigenwerte werden um 0 herum gesucht)
	
    dseupd_(&rvec, "All", sel, eigvals, eigvecs, &n, &sigma,
        "I", &n, "LM", &nev, &tol, resid, &ncv,
        vmat, &ldv, iparam, ipntr, workd, workl, &lworkl, &info);
		
	printf("Final Info (dseupd_): %d\n", info);	
	
	FILE *eigenvals = fopen("eigenvals.txt", "w");
    for (int i = 0; i < nev; i++){
        printf("eigval[%d] %.10f \n", i, eigvals[i]*1/eigvals[0]);    //eigenwerte wurden relativ zum ersten eigenwert normiert
		fprintf(eigenvals, "%d %.10f \n", i, eigvals[i]*1/eigvals[0]);
    }
	
	FILE *eigenvecs = fopen("eigenvecs.txt", "w");
    for (int j = 0; j < nev; j++){

        for (int i = 0; i < n; i++){
			
            double y = fm(eigvecs, i, j, n); 
			fprintf(eigenvecs,"%.15e ", y);
			
        }
        fprintf(eigenvecs, "\n");
    }
    fflush(eigenvecs);
    fclose(eigenvecs);
	
    free(resid);
    free(vmat);
    free(workd);
    free(workl);
    free(sel);
    free(eigvals);
    free(eigvecs);
}









