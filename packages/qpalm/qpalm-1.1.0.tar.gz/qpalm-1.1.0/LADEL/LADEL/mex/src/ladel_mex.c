#include "mex.h"
#include "matrix.h"
#include <string.h>
#include "ladel.h"
#include "ladel_mex_util.h"

/* Modes of operation */
#define MODE_INIT "init"
#define MODE_FACTORIZE_REGULAR "factorize"
#define MODE_FACTORIZE_ADVANCED "factorize_advanced"
#define MODE_FACTORIZE_WITH_PRIOR_BASIS "factorize_with_prior_basis"
#define MODE_ROW_MOD "rowmod"
#define MODE_DENSE_SOLVE "solve"
#define MODE_DELETE "delete"
#define MODE_RETURN "return"

/* LADEL work identifier */
static ladel_work* work = NULL;
static ladel_symbolics *sym = NULL;
static ladel_factor *LD = NULL;

/* Use Mex's custom allocators */
static void *ladel_mex_calloc(size_t n, size_t size) {
    void *m = mxCalloc(n, size);
    mexMakeMemoryPersistent(m);
    return m;
}
static void *ladel_mex_malloc(size_t size) {
    void *m = mxMalloc(size);
    mexMakeMemoryPersistent(m);
    return m;
}
static void* ladel_mex_realloc(void *p, size_t size) {
    void *p_new = mxRealloc(p, size);
    mexMakeMemoryPersistent(p_new);
    return p_new;
}
static void ladel_mex_free(void* p) {
    mxFree(p);
}

struct {
    calloc_sig *calloc;
    malloc_sig *malloc;
    realloc_sig *realloc;
    free_sig *free;
    printf_sig *printf;
} static old_config = {
    .calloc = NULL,
    .malloc = NULL,
    .realloc = NULL,
    .free = NULL,
    .printf = NULL
};

static int config_configured = 0;

static void configure_mex_specific_functions(void) {
    if (config_configured)
        return;
    config_configured = 1;
    old_config.calloc = ladel_set_alloc_config_calloc(&ladel_mex_calloc);
    old_config.malloc = ladel_set_alloc_config_malloc(&ladel_mex_malloc);
    old_config.realloc = ladel_set_alloc_config_realloc(&ladel_mex_realloc);
    old_config.free = ladel_set_alloc_config_free(&ladel_mex_free);
    old_config.printf = ladel_set_print_config_printf(&mexPrintf);
}

static void unconfigure_mex_specific_functions(void) {
    if (old_config.calloc) {
        ladel_set_alloc_config_calloc(old_config.calloc);
        old_config.calloc = NULL;
    }
    if (old_config.malloc) {
        ladel_set_alloc_config_malloc(old_config.malloc);
        old_config.malloc = NULL;
    }
    if (old_config.realloc) {
        ladel_set_alloc_config_realloc(old_config.realloc);
        old_config.realloc = NULL;
    }
    if (old_config.free) {
        ladel_set_alloc_config_free(old_config.free);
        old_config.free = NULL;
    }
    if (old_config.printf) {
        ladel_set_print_config_printf(old_config.printf);
        old_config.printf = NULL;
    }
}

/* Mex calls this when it closes unexpectedly, freeing the workspace */
void exitFcn() {
  if (work != NULL) {
      ladel_workspace_free(work);
      work = NULL;
  }
  if (config_configured) {
      unconfigure_mex_specific_functions();
  }
}

/**
 * The gateway function to LADEL
 *
 * Usages:
 * ladel_mex('init', ncol);
 * ladel_mex('factorize', M);
 * ladel_mex('factorize', M, ordering);
 * [L, D] = ladel_mex('return');
 * [L, D, p] = ladel_mex('return');
 * ladel_mex('factorize_advanced', M, Mbasis);
 * ladel_mex('factorize_advanced', M, Mbasis, ordering);
 * ladel_mex('factorize_with_prior_basis', M);
 * ladel_mex('rowmod', row_index);
 * ladel_mex('rowmod', row_index, row, diag_elem);
 * y = ladel_mex('solve', x);
 * ladel_mex('delete');
 *
 * @param nlhs Number of output arguments
 * @param plhs Array of output argument pointers
 * @param nrhs Number of input arguments
 * @param prhs Array of input argument pointers
 */
void mexFunction(int nlhs, mxArray * plhs [], int nrhs, const mxArray * prhs []) {
    
    /* Set function to call when mex closes unexpectedly */
    mexAtExit(exitFcn);

    /* Set the custom allocator and print functions */
    configure_mex_specific_functions();

    /* Ignore the self/obj pointer */
    --nrhs;

    /* Get the command string */
    char cmd[64];
    
    // strcpy(factorize_advanced, "factorize_advanced");
    if (nrhs < 1 || mxGetString(prhs[1], cmd, sizeof(cmd)))
		mexErrMsgTxt("First input should be a command string less than 64 characters long.");

    if (strcmp(cmd, MODE_INIT) == 0) 
    {
        /* Warn if other commands were ignored */
        if (nrhs != 2)
            mexErrMsgTxt("Wrong number of input arguments for mode init.");
        
        if (work != NULL)
            mexErrMsgTxt("Work is already initialized.");

        ladel_int ncol = (ladel_int) *mxGetPr(prhs[2]);
        work = ladel_workspace_allocate(ncol);
        sym = ladel_symbolics_alloc(ncol);
        return;
    } 
    else if (strcmp(cmd, MODE_DELETE) == 0) 
    {    
        /* clean up the problem workspace */
        if(work != NULL){
            work = ladel_workspace_free(work);
            sym = ladel_symbolics_free(sym);
            LD = ladel_factor_free(LD);
        }
        /* Warn if other commands were ignored */
        if (nlhs != 0 || nrhs != 1)
            mexWarnMsgTxt("Delete: Unexpected arguments ignored.");
        return;

    } 
    else if (strcmp(cmd, MODE_DENSE_SOLVE) == 0)
    {
        if (nlhs != 1 || nrhs != 2 )
            mexErrMsgTxt("Wrong number of input or output arguments for mode solve.");

        plhs[0] = mxCreateDoubleMatrix(LD->ncol,1,mxREAL);
        ladel_double *y = mxGetPr(plhs[0]); 
        ladel_double *x = mxGetPr(prhs[2]); 
        ladel_dense_solve(LD, x, y, work);

        return;
    }
    else if (strcmp(cmd, MODE_RETURN) == 0)
    {
        if (nlhs != 2 && nlhs != 3)
            mexErrMsgTxt("Wrong number of output arguments for mode return.");

        if (LD == NULL)
            mexErrMsgTxt("No factors to return.");

        ladel_sparse_matrix *L_sparse = ladel_convert_factor_to_sparse(LD->L);
        plhs[0] = ladel_put_matlab_from_sparse(L_sparse);

        plhs[1] = mxCreateDoubleMatrix(LD->ncol, 1, mxREAL);
        double *D = mxGetPr(plhs[1]);
        ladel_int index;
        for (index = 0; index < LD->ncol; index++) D[index] = (double) 1.0/LD->Dinv[index];

        if (nlhs == 2 && LD->p != NULL)
            mexWarnMsgTxt("Factor has permutation but this is not requested in the output arguments.");
        if (nlhs == 3)
        {
            plhs[2] = mxCreateDoubleMatrix(LD->ncol, 1, mxREAL);
            double *p = mxGetPr(plhs[2]);
            if (LD->p != NULL)
                for (index = 0; index < LD->ncol; index++) p[index] = (double) LD->p[index]+1;
            else
                for (index = 0; index < LD->ncol; index++) p[index] = (double) index+1;                   
        }
        return;     
    }
    else if (strcmp(cmd, MODE_ROW_MOD) == 0)
    {
        if (nlhs != 0 || (nrhs != 3 && nrhs != 5))
            mexErrMsgTxt("Wrong number of input or output arguments for mode row_mod.");

        if (LD == NULL)
            mexErrMsgTxt("Row_mod: No factor found. First use factorize_advanced to compute L and D.");

        ladel_int* rows_in_L = (ladel_int*) mxGetData(prhs[2]);
        ladel_int nb_rows = (ladel_int) mxGetScalar(prhs[3]);
        
        ladel_int status, index;
        if (nrhs == 3)
        {
            for (index = 0; index < nb_rows; index++)
            {
                status = ladel_row_del(LD, sym, --(rows_in_L[index]), work);
                if (status != SUCCESS)
                    mexErrMsgTxt("Row_mod: Something went wrong in updating the factorization.");
            }
        } 
        else if (nrhs == 5)
        {
            ladel_sparse_matrix Wmatlab;
            ladel_sparse_matrix *W = ladel_get_sparse_from_matlab(prhs[4], &Wmatlab, UNSYMMETRIC);
            /* To not modify the matlab argument in place, we have to copy it */
            ladel_sparse_matrix *W_copy = ladel_sparse_allocate_and_copy(W);
            ladel_double* diag = mxGetPr(prhs[5]);

            for (index = 0; index < nb_rows; index++)
            {
                status = ladel_row_add(LD, sym, --(rows_in_L[index]), W_copy, index, diag[index], work);
                if (status != SUCCESS)
                {
                    W_copy = ladel_sparse_free(W_copy);
                    mexErrMsgTxt("Row_mod: Something went wrong in updating the factorization.");
                }
            }
        }

        return;
    }
    else if (strcmp(cmd, MODE_FACTORIZE_REGULAR) == 0)
    {
        if (nlhs != 0 || (nrhs != 2 && nrhs != 3))
            mexErrMsgTxt("Wrong number of input or output arguments for mode factorize.");

        if (LD != NULL) LD = ladel_factor_free(LD);

        ladel_sparse_matrix Mmatlab;
        ladel_sparse_matrix *M = ladel_get_sparse_from_matlab(prhs[2], &Mmatlab, UPPER);
        ladel_int ordering;
        if (nrhs == 3)
            ordering = (ladel_int) *mxGetPr(prhs[3]);
        else
            ordering = NO_ORDERING;
        
        ladel_int status = ladel_factorize(M, sym, ordering, &LD, work);
        if (status != SUCCESS)
            mexErrMsgTxt("Factorize: Something went wrong in the factorization.");

        return;
    }
    else if (strcmp(cmd, MODE_FACTORIZE_ADVANCED) == 0)
    {
        if (nlhs != 0  || (nrhs != 3 && nrhs != 4))
            mexErrMsgTxt("Wrong number of input or output arguments for mode factorize_advanced.");

        if (LD != NULL) LD = ladel_factor_free(LD);

        ladel_sparse_matrix Mmatlab;
        ladel_sparse_matrix *M = ladel_get_sparse_from_matlab(prhs[2], &Mmatlab, UPPER);

        ladel_sparse_matrix Mbasismatlab;
        ladel_sparse_matrix *Mbasis = ladel_get_sparse_from_matlab(prhs[3], &Mbasismatlab, UPPER);

        ladel_int ordering;
        if (nrhs == 4)
            ordering = (ladel_int) *mxGetPr(prhs[4]);
        else
            ordering = NO_ORDERING;
        

        ladel_int status = ladel_factorize_advanced(M, sym, ordering, &LD, Mbasis, work);
        if (status != SUCCESS)
            mexErrMsgTxt("Factorize_advanced: Something went wrong in the factorization.");

        return;
    }
    else if (strcmp(cmd, MODE_FACTORIZE_WITH_PRIOR_BASIS) == 0)
    {
        if (nlhs != 0  || (nrhs != 2))
            mexErrMsgTxt("Wrong number of input or output arguments for mode factorize_with_prior_basis.");

        ladel_sparse_matrix Mmatlab;
        ladel_sparse_matrix *M = ladel_get_sparse_from_matlab(prhs[2], &Mmatlab, UPPER);
       
        ladel_int status = ladel_factorize_with_prior_basis(M, sym, LD, work);
        if (status != SUCCESS)
            mexErrMsgTxt("Factorize_with_prior_basis: Something went wrong in the factorization.");

        return;
    }
    else 
    {
        mexErrMsgTxt("Invalid LADEL mode");
        return;
    }
}