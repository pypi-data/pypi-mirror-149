import os
import wget
from pyomo.environ import *
import numpy as np
from zipfile import ZipFile

import os
import wget
from pyomo.environ import *
import numpy as np
from zipfile import ZipFile


def kelley_optimizer( returns, varcov, rfr, ipopt_directory=None):
    '''
    Parameters
    ----------
    returns : list
        list of expected pnl
    varcov : square matrix
        variance covariance matrix
    rfr : float
        risk free rate
    ipopt_directory : str/None
        filepath of executable ipopt solver

    Returns
    -------
    kelley_mults : list
        list of kelley criterion
        wieghting for each strategy

    Example
    -------
    returns = np.array([0.0476, 0.004]) # mu
    varcov = np.matrix([[2.12, 1.03], # sigma_ij
                [1.03, 1.89]])

    Solver to use
    !wget -N -q "https://ampl.com/dl/open/ipopt/ipopt-linux64.zip"
    !unzip -o -q ipopt-linux64

    Reference & Credit
    ------------------
    https://medium.com/raposa-technologies/how-to-use-python-and-the-kelly-criterion-to-optimize-your-stock-portfolio-bb6e43df50c2
    '''


    if ipopt_directory is None:
        fp_executable = os.path.join( os.path.dirname(os.path.abspath(__file__ ) ), 'ipopt' )
        if not os.path.exists(fp_executable):
            fp_executable = download_solver()
    else:
        fp_executable = download_solver(ipopt_directory)

    print(f'solver: {fp_executable}')
    model = buildKCOptModel(returns, varcov, rfr)
    results = SolverFactory('ipopt', executable=fp_executable).solve(model)
    print(f"g = {model.objective.expr():.3f}")
    print(f"Fractions = {[np.round(model.f[i].value, 3) for i in model.i]}")
    portfolio_weights = [model.f[i].value for i in model.i]
    return portfolio_weights

def buildKCOptModel(returns: np.array, varcov: np.matrix,
                    rfr: float = 0):
    assert returns.shape[0] == varcov.shape[0]
    assert returns.shape[0] == varcov.shape[1]

    m = ConcreteModel()

    # Indices
    m.i = RangeSet(0, returns.shape[0] - 1)

    # Decision variables
    m.f = Var(m.i, domain=UnitInterval)

    # Parameters
    m.mu = Param(m.i,
               initialize={i: m for i, m in zip(m.i, returns)})
    m.sigma = Param(m.i, m.i,
                  initialize={(i, j): varcov[i, j]
                              for i in m.i
                              for j in m.i})

    # Constraints
    @m.Constraint()
    def fullyInvestedConstraint(m):
        return sum(m.f[i] for i in m.i) == 1

    # Objective
    @m.Objective(sense=maximize)
    def objective(m):
        return (rfr + sum(m.f[i] * (m.mu[i] - rfr) for i in m.i) - \
            sum(
                sum(m.f[i] * m.sigma[i, j] * m.f[j] for j in m.i)
            for i in m.i) / 2)

    return m

def download_solver(output_directory=None):

    if output_directory is None:
        print('downloading solver to home...')
        output_directory = os.path.dirname(os.path.abspath(__file__ ) )

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    print(output_directory)
    fp = os.path.join(output_directory, 'ipopt')

    if not os.path.exists( fp ):

        url = "https://ampl.com/dl/open/ipopt/ipopt-linux64.zip"
        filename = wget.download(url, out=output_directory)

        with ZipFile(filename) as archive:

            archive.extractall(output_directory)
            fp = os.path.join(output_directory, 'ipopt')
            try:
                # make executable
                os.system( f'chmod +x {fp}')
            except:
                pass

    return fp
