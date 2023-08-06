'''
mcreep.func
-----------
Definition of functions for fitting.

* The functions are defined in general form:`deformation(t) = f(t)`
* The package fits the functions to both tensile and indentation creep data.
'''

import numpy as np

def power_law(t, c, k):
    '''
    Function defining PL model (Power Law model).
        
    Parameters
    ----------
    t : float
        Time = X-variable for fitting.
    
    c, k : float, float
        Parameters of power law model.

    Returns
    -------
    Function = expression for fitting procedure.
    
    '''
    # Define fitting function - here - power law
    func = c * t**k
    # Return final function
    return(func)

def evp_s_d_1kv(t, const,B0,Cv, D1,tau1):
    '''
    Function defining EVP model with elements [S + D + 1*KV].

    Parameters
    ----------
    t : float
        Time = X-variable for fitting.

    const : float
        Multiplicative constant for EVP models.
        
        * Tensile experiments: const = applied stress = sigma[GPa]
            - For sample calculation of sigma,
              see mcreep.const.Experiment object.
        * Indentation experiments: const = F*K
            - F[mN] = loading force
            - K for point indenters = pi/(2*tan(alpha))
            - K for spherical indenters = 3/(4*sqrt(R))

    B0 : float
        Parameter corresponding to S-element of EVP model.

    Cv : float
        Parameter corresponding to D-element of EVP model.

    D1 : float
        Parameter of KV-element of EVP model ~ compliance.

    tau1 : float
        Parameter of KV-element of EVP model = retardation time.
    
    Returns
    -------
    Function = expression for fitting procedure.
    
    '''
    # Define model function (constants will be fixed later)
    func = const * (B0 + Cv*t - D1*np.exp(-t/tau1))
    # Return final function
    return(func)

def evp_s_d_2kv(t, const,B0,Cv, D1,D2, tau1,tau2):
    '''
    Function defining EVP model with elements [S + D + 2*KV].

    Parameters
    ----------
    t : float
        Time = X-variable for fitting.

    const : float
        Multiplicative constant for EVP models.
        
        * Tensile experiments: const = applied stress = sigma[GPa]
            - For sample calculation of sigma,
              see mcreep.const.Experiment object.
        * Indentation experiments: const = F*K
            - F[mN] = loading force
            - K for point indenters = pi/(2*tan(alpha))
            - K for spherical indenters = 3/(4*sqrt(R))

    B0 : float
        Parameter corresponding to S-element of EVP model.

    Cv : float
        Parameter corresponding to D-element of EVP model.

    D1, D2 : float, float
        Parameters of KV-elements of EVP model ~ compliance.

    tau1, tau2 : float, float
        Parameters of KV-elements of EVP model = retardation times.
    
    Returns
    -------
    Function = expression for fitting procedure.
    
    '''
    # Define model function (constants will be fixed later)
    func = const * (B0 + Cv*t - (D1*np.exp(-t/tau1) + D2*np.exp(-t/tau2)))
    # Return final function
    return(func)


def evp_s_d_3kv(t, const,B0,Cv, D1,D2,D3, tau1,tau2,tau3):
    '''
    Function defining EVP model with elements [S + D + 3*KV].

    Parameters
    ----------
    t : float
        Time = X-variable for fitting.

    const : float
        Multiplicative constant for EVP models.
        
        * Tensile experiments: const = applied stress = sigma[GPa]
            - For sample calculation of sigma,
              see mcreep.const.Experiment object.
        * Indentation experiments: const = F*K
            - F[mN] = loading force
            - K for point indenters = pi/(2*tan(alpha))
            - K for spherical indenters = 3/(4*sqrt(R))

    B0 : float
        Parameter corresponding to S-element of EVP model.

    Cv : float
        Parameter corresponding to D-element of EVP model.

    D1, D2, D3 : float, float, float
        Parameters of KV-elements of EVP model ~ compliance.

    tau1, tau2, tau3 : float, float, float
        Parameters of KV-elements of EVP model = retardation times.
    
    Returns
    -------
    Function = expression for fitting procedure.
    
    '''
    # Define model function (constants will be fixed later)
    func = const * (B0 + Cv*t - (
        D1*np.exp(-t/tau1) + D2*np.exp(-t/tau2) + D3*np.exp(-t/tau3)))
    # Return final function
    return(func)
