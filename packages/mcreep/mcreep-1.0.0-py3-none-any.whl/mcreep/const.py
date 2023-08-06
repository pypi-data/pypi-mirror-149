'''
mcreep.const
------------
Global constants for package mcreep.

* The global constants are saved in the form of objects.
* Reason: some parameters must be [re]defined during initialization.
'''

from math import pi,sqrt,tan
import matplotlib.pyplot as plt

class Experiment:
    '''
    Experiment = object describing the creep experiment.
    
    Parameters
    ----------
    
    etype : str; which takes one o the following values
        * 'Tensile' = (macroscale) tensile creep experiment
        * 'Vickers' = (micro/nanoscale) indentation creep with Vickers tip
        * 'Berkovich' = (micro/nanoscale) indentation creep with Berkovich tip
        * 'Spherical' = (micro/nanoscale) indentation creep with spherical tip
    
    F : float; optional, default is None
        Loading force during indentatin experiments in [mN].
        Relevant (and obligatory) for etype='Vickers/Berkovich/Spherical'.
    
    R : float; optional, the default is None
        Radius of spherical tip in [um].
        Relevant (and obligatory) for etype='Spherical'.
    
    sigma : float; optional, default is None
        Stress during tensile experiments in [GPa].
        Relavant (and obligatory) for etype='Tensile'.
        
        Sample calculation of sigma (for tensile experiments at IMC):
            
        * `sigma[GPa] = (load[kg]*sa*g[m/s2]) / (W[mm]*T[mm]/1e6) / 1e9`
        * sa = stress amplifier (optional lever amplifying the load)
        * g = net acceleration = gravity of Earth = 9.81[m/s2]
        * W,T = width and thickness of testing specimen in [mm]
        * 1e6 = recalculate W*T[mm2] -> [m2]
        * 1e9 = recalculate final result [Pa] -> [GPa] 
    '''
    
    def __init__(self, etype, F=None, R=None, sigma=None):
        # Docstring for __init__ are given above in class description.
        # Reason: In this way, the parameters are visible in Spyder/Ctrl+I.
        
        # (1) Initialize basic parameters
        self.etype = etype
        self.F = F
        self.R = R
        self.sigma = sigma
        # (2) Calculate additional parameters: K,m
        # (parameters K,m calculated according to {Mencik 2011}
        # {Mencik 2011} = Polymer Testing 30 (2011) 101–109; Eq.(9) at p.103.
        if self.etype == 'Tensile':
            self.K = 1
            self.m = 1
        elif self.etype in ['Vickers','Berkovich']:
            alpha = 70.3 * pi/180
            self.K = pi/(2*tan(alpha))
            self.m = 2
        elif self.etype == 'Spherical':
            self.K = 3/(4*sqrt(self.R))
            self.m = 3/2
        # (3) Calculate additional parameter: const
        # (const is employed in EVP models,
        # (...in which it is the 1st multiplicative constant
        # (...that differs for tensile and indentation experiments;
        # (this is my generalization, which enables that the package
        # (...can be used for both tensile and indentation experiments        
        if self.etype == 'Tensile':
            self.const = self.sigma
        elif self.etype in ['Vickers','Berkovich','Spherical']:
            self.const = self.F*self.K

class DataParameters:
    '''
    DataParameters = object defining creep datafile.
    Assumption: creep datafile contains columns of data,
    namely times and deformations.
    
    Parameters
    ----------
    
    usecols : list with two integer values; optional, the default is [0,1]
        This parameter is passed to numpy.loadtxt.
            * The 1st value of the list = column with times.
            * The 2nd value of the list = column with deformations.
    
    comments : string or sequence of strings; optional, the default is '#'
        This parameter is passed to numpy.loadtxt.
        The character(s) indicate comment/ignored lines in input datafile.
    
    skiprows : integer; optional, the default is 1
        This parameter is passed to numpy.loadtxt.
        The first {skiprows} lines are skipped.
    
    time_to_seconds : float; optional, the default is 1
        Multiplicative constant, which converts time values to seconds.
    
    deformation_to_um : float; optional, the default is 1
        Multiplicative constant, which converts deformations to micrometers.
    '''
    
    def __init__(self, usecols=[0,1], comments='#', skiprows=0,
                 time_to_seconds=1, deformation_to_um=1):
        # Docstring for __init__ are given above in class description.
        # Reason: In this way, the parameters are visible in Spyder/Ctrl+I.
        
        self.usecols = usecols
        self.comments = comments
        self.skiprows = skiprows
        self.time_to_seconds = time_to_seconds
        self.deformation_to_um = deformation_to_um
        
class PlotParameters:
    '''
    PlotParameters = object defining local+global parameters for plotting.
    
    Parameters
    ----------
    
    xlabel, ylabel : str, str
        Labels for X and Y axis.

    logscale : bool; optional, the default is False
        If logscale==True, both X and Y axes are in logarithmic scale.

    e_to_percent : bool; optional, the default is True
        Relevant only to tensile experiments.
        If true, the values of elongation are multiplied by 100,
        i.e. they are converted from epsilon[] to epsilon[%].
        
    rcParams : dict; optional, the default is empty dictionary {}
        The dictionary shoud be formatted for mathplotlib.pyplot.rcParams.
        The argmument is passed to matplotlib.pyplot.
        The initialization procedure creates some default rcParams.
        This argument can override this pre-defined parameters,
        i.e. the default is created anyway
        and then (possibly) supplemented by rcParams argument.
    '''
    
    def __init__(self, xlabel, ylabel,
                 logscale=False, e_to_percent=True, rcParams={}):
        # Docstring for __init__ are given above in class description.
        # Reason: In this way, the parameters are visible in Spyder/Ctrl+I.
        
        # Initialize basic parameters
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.logscale = logscale
        self.e_to_percent = e_to_percent
        self.rcParams = rcParams
        # Set global plot settings using rcParams
        plt.rcParams.update({
            'figure.figsize'     : (8/2.54,6/2.54),
            'figure.dpi'         : 500,
            'font.size'          : 7,
            'lines.linewidth'    : 0.8,
            'axes.linewidth'     : 0.6,
            'xtick.major.width'  : 0.6,
            'ytick.major.width'  : 0.6,
            'grid.linewidth'     : 0.6,
            'grid.linestyle'     : ':'})
        # Adjust global plot settings if argument rcParams was defined
        plt.rcParams.update(self.rcParams)
