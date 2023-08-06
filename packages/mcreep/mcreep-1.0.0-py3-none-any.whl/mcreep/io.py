'''
mcreep.io
-----------
Input/output functions for package mcreep.    
'''

import sys
import numpy as np
import matplotlib.pyplot as plt

def read_datafile(MODEL, datafile, t_start, t_hold):
    '''
    Read datafile containing creep data.
    
    Parameters
    ----------
    MODEL : MODEL object
        * The object keeps experiment parameters in MODEL.EPAR property.
        * We use the object to convert time and deformation to correct units.
    datafile : string or pathlib object
        Name of datafile = text file containing two columns (t,h).
    t_start : float
        Start of step II = holding step = period at which F = Fmax.
    t_end : float
        End of step II = holding step = period at which F = Fmax.
        
    Returns
    -------
    2D numpy array
    
    Expected format of the datafile
    -------------------------------
        * Two colums (t,h) separated by whitespace.
        * 1st column = t[s] = time in seconds
        * 2nd column = deformation[um] = deformation in micrometers
        * ...in tensile experiments: deformation = strain
        * ...in indentation experiments: deforamtion = penetration depth
    '''
    
    # Read file to numpy array and try to catch possible errors/exceptions
    try:
        # read h-t file
        data = np.loadtxt(
            datafile, unpack=True,
            usecols = MODEL.DPAR.usecols,
            skiprows = MODEL.DPAR.skiprows,
            comments = MODEL.DPAR.comments)
        # take just section II of h-t curve
        # section I = loading  = (0..t_start] ...without 0 due to logarithms
        # section II = holding = [t_start..t_hold] ...time of maximal loading
        data = data[:,(data[0]>t_start) & (data[0]<(t_start+t_hold))]
        # recalculate time and deformation to [s] and [um], respectively
        data[0] = data[0] * MODEL.DPAR.time_to_seconds
        data[1] = data[1] * MODEL.DPAR.deformation_to_um
    except OSError as err:
        print('OSError:', err)
        sys.exit()
    except ValueError:
        print('ValueError: probably a wrong format of the file.')
        print('Expected format: TXT file with two columns t[s], h[nm]')
        sys.exit()
    # Return final 2D numpy array
    # (1st column = t[s], 2nd column = h[um], range = [t_start;t_start+t_hold]
    return(data)

def print_fitting_result(MODEL, datafile, par):
    '''
    Print ONE result of fitting
    (i.e. print fitting results for one/currently processed datafile).

    We note that the complete results of fitting (for all datafiles)
    are kept in mcreep.model.Model object and usually reported/printed
    together at the very end of the whole processing.

    Parameters
    ----------
    MODEL : mcreep.model.Model object
        This object contains all properties needed to print the result.
        
    datafile : str
        Name of the datafile;
        in this procedure, it is just printed to stdout
        in order to denote the source of the fitting results.
        
    par : list of floats
        List of optimized parameters of given fitting function;
        output from the procedure mcreep.fit.fit.

    Returns
    -------
    None. The output are results printed on stdout.

    '''
    # (1) Convert parameters array to tuple => suitable for formatted printing 
    par = tuple(par)
    # (2) Print datafile name (this is the same for all models)
    print(f'{datafile:12s}', end='')
    # (3) Print parameters of individual models...
    if MODEL.fname == 'power_law':
        print('[c,k]: %8.4f %8.4f' % par)
    elif MODEL.fname == 'evp_s_d_1kv':
        if MODEL.rtimes:
            print('[B0,Cv,D1]: %8.4f %8.4f %8.4f' % par)
        else:
            print('[B0,Cv,D1,tau1]: %8.4f %8.4f %8.4f %6.2f' % par) 
    elif MODEL.fname == 'evp_s_d_2kv':
        if MODEL.rtimes:
            print('[B0,Cv,D1,D2]: ', end='')
            print('%8.4f %8.4f %8.4f %8.4f' % par)
        else:
            print('[B0,Cv,D1,D2,tau1,tau2]: ', end='')
            print('%8.4f %8.4f %8.4f %8.4f %6.2f %6.2f' % par) 
    elif MODEL.fname == 'evp_s_d_3kv':
        if MODEL.rtimes:
            print('[B0,Cv,D1,D2,D3]: ',end='')
            print('%8.4f %8.4f %8.4f %8.4f %8.4f' % par)
        else:
            print('[B0,Cv,D1,D2,D3,tau1,tau2,tau3]: ', end='')
            print('%8.4f %8.4f %8.4f %8.4f %8.4f %6.2f %6.2f %6.2f' % par)
    else:
        print('Warning: unknown model during printing!')
        print(par)

def plot_result(MODEL, data, par, output_graph):
    '''
    Plot ONE result of fitting
    (i.e. create plot for one/currently processed datafile).

    Parameters
    ----------
    MODEL : TYPE
        DESCRIPTION.
    data : TYPE
        DESCRIPTION.
    par : TYPE
        DESCRIPTION.
    output_graph : TYPE
        DESCRIPTION.
        
    Parameters
    ----------
    MODEL : mcreep.model.Model object
        This object contains all properties needed to print the result.
        
    data : 2D numpy array
        Creep data read from the currently processed datafile.
        
    par : list of floats
        List of optimized parameters of given fitting function;
        output from the procedure mcreep.fit.fit.
    
    output_graph : str or path-like object
        Name of the file containing the output graph.

    Returns
    -------
    None. The output graph is shown (plt.show) and saved (to output_file).
    
    '''
    # (1) Read data
    X,Y  = data
    # (2) Calculate fitted data
    # Trick: *(list(par)) = convert saved parameters to list and expand
    Yfit = MODEL.func(X, *(list(par)))
    # (3) For tensile experiments, convert elongation to % if required.
    if MODEL.EPAR.etype == 'Tensile' and MODEL.PPAR.e_to_percent == True:
        Y = Y*100
        Yfit = Yfit*100
    # (4) Recalculate fitting function
    # Reason: Tensile x Indentation experiments fit different deformations...
    # More details => see the description of the recalculating fucntion.
    Yfit = recalculate_fitted_data(MODEL.EPAR, Yfit)
    # (5) If required, convert data to logscale
    # AND change x/ylabels accordingly.
    if MODEL.PPAR.logscale == True:
        # (a) Convert data to logscale
        X = np.log10(X)
        Y = Y = np.log10(Y)
        Yfit = np.log10(Yfit)
        # (b) change x/ylabels
        # Trick: this function is called repeatedly
        # => check if the change of x/ylabes has not been already done!
        if not(MODEL.PPAR.xlabel.startswith('log')):
            MODEL.PPAR.xlabel = 'log('+MODEL.PPAR.xlabel+')'
        if not(MODEL.PPAR.ylabel.startswith('log')):
            MODEL.PPAR.ylabel = 'log('+MODEL.PPAR.ylabel+')'
    # (6) Create plot
    # (user-adjustable + global plot settings are saved in PPAR object
    # (MODEL.PPAR object is an instance of mcreep.const.PlotParameters class
    plt.plot(X, Y, color='orange', label='Experiment')
    plt.plot(X, Yfit, 'k:', label=MODEL.name)
    plt.xlabel(MODEL.PPAR.xlabel)
    plt.ylabel(MODEL.PPAR.ylabel)
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_graph)
    plt.show()

def recalculate_fitted_data(EPAR, Yfit):
    '''
    Recalculation of the fitted data before plotting.
   
    Parameters
    ----------
    EPAR : Experiment object.
        Object with experimental parameters (here we need EPAR.m).
    Yfit : 1D numpy array.
        Original Y-data that were fitted,
        BUT we fit various types of data (epsilon, h**2, h**3/2)
        WHEREAS we always want to plot deformation (without powers).
        See also {Reason for the recalculation} section below.

    Returns
    -------
    Yfit : 1D numpy array.
        Recalculated Y-data for plotting.

    Reason for the recalculation
    ----------------------------
    Fitting function f(t) fits different types of deformation...
    
    * ...Tensile creep: deformation(t) = epsilon(t) = f(t)
    * ...Indentation (Vickers,Berkovich): deformation(t) = h**2(t) = f(t)
    * ...Indentation (Spherical tip): deformation(t) = h**(3/2)(t) = f(t)
    
    Therefore, there are powers of deformation, but we plot just deformation.
    
    Consequently, the recalculations must be done as follows:
    
    * ...Tensile creep: no recalculation
    * ...Indentation (Vickers,Berkovich): Yfit = Yfit**(1/2)
    * ...Indentation (Spherical tip): Yfit = Yfit**(2/3)
    '''
    if EPAR.etype != 'Tensile': Yfit = Yfit ** (1/EPAR.m)
    return(Yfit)