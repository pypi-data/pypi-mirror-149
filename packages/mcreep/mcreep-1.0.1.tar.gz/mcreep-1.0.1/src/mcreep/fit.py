'''
mcreep.fit
-----------
Fitting of creep curves + statistics of fitting.  
'''

import sys
import numpy as np
from scipy import optimize

def fit(MODEL, data, t_fstart, t_fend):
    '''
    Fit [creep data] to [MODEL].

    Parameters
    ----------
    MODEL : mcreep.model.Model object
        This object contains all properties needed to print the result.
        For this function, the most important are
        experimental parameters (MODEL.EPAR)
        and fitting function (MODEL.func).
    
    data : 2D numpy array
        Numpy array containing two columns with creep data
        (time and deformation).
        We note that this procedure is universal and fits data from
        both indentation and tensile creep experiments
        (see code below and comments inside it).
    
    t_fstart, t_fend : float, float
        The creep data are fitted to model function in interval
        [t_fstart; t_fend].
    
    Returns
    -------
    par,cov : list, list
        List parameters and their covariances for given fitting function
        (output from function scipy.optimize.curve_fit).
    
    '''
    # Cut data with t < t_fit
    data = data[:,(t_fstart<=data[0])&(data[0]<=t_fend)]
    # Split data into X,Y = t[s],h[um]
    X = data[0]
    Y = data[1]
    # Recalculate deformation data according to experiment type
    Y = recalculate_deformation(MODEL.EPAR, Y)
    # Fit data with given function
    # (Trick: we employ MODEL.iguess as initial guess of parameters
    # (...if iguess is not given, its default value None is used - Ok
    par,cov = optimize.curve_fit(MODEL.func,X,Y, p0=MODEL.iguess)
    # Return result
    return(par,cov)

def recalculate_deformation(EPAR,Y):
    '''
    Recalculation of deformation
    so that it could be fitted with model function.
    
    The model function fit different types of deformation,
    depending on the type of creep experiment:
        
    * Model.EPAR.etype == 'Tensile' => deformation = strain = epsilon
    * Model.EPAR.etype == 'Vickers' or 'Berkovich' => deformation = h**2
    * Model.EPAR.etype == 'Spherical' => deformation = h**3/2
    
    In general, the indentation creep fits h(t)**m.
    The constant m is saved in Model.EPAR.m.

    Parameters
    ----------
    EPAR : Experiment object
        Experiment object contains information about creep experiment.
        In this function, we need EPAR.m, which is used for h recalculation.
        
    Y : numpy array
        Deformation data for fitting.
        This data must be recalculated, as explained above.

    Returns
    -------
    Y : numpy array
        Y-data (= deformation) for fitting.
        The data are recalculated as necessary.

    '''
    if EPAR.etype == 'Tensile':
        pass
    elif EPAR.etype in ('Vickers','Berkovich','Spherical'):
        Y = Y**(EPAR.m)
    else:
        sys.exit('Unknown model!')
    return(Y)

def coefficient_of_determination(MODEL, par, data):
    '''
    Calculate R2 = coefficient of determination.
    R2 characterizes how well the data are predicted by fitting function.    

    Parameters
    ----------
    MODEL : mcreep.model.Model object
        This object contains all properties for calculation.
        
    par : list of floats
        Parameters of the fitting function
        (output from mcreep.fit.fit function).

    data : 2D numpy array
        Creep data used for fitting.
        Coefficient of determination is calculated from original data
        and fitted function (which is re-constructed from MODEL.func + par).

    Returns
    -------
    R2 : float
        Calculated coefficient of determination.

    '''
    # Coefficient of determination = R2
    # R2 values: 1 = perfect, 0 = estimate ~ average(Y), negative = very bad 
    # https://en.wikipedia.org/wiki/Coefficient_of_determination
    X = data[0]
    Y = data[1]
    # Recalculate deformation data according to experiment type
    Y = recalculate_deformation(MODEL.EPAR, Y)
    Yave = np.average(Y)
    Yfit = MODEL.func(X,*par)
    SSres = np.sum((Y-Yfit)**2)
    SStot = np.sum((Y-Yave)**2)
    R2 = 1 - SSres/SStot
    return(R2)