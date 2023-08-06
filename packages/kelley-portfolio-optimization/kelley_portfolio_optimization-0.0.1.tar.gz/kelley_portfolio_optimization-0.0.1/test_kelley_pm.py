import os
import sys

import numpy as np

fp = os.path.dirname(os.path.abspath( __file__ ))
fpp = os.path.join(fp, 'src')
sys.path.insert(0 , fpp)
from kelley_portfolio_optimization import kelley_optimizer

def test_kelley_optimizer():
    returns = np.array([0.0476, 0.004]) # mu
    varcov = np.matrix([[2.12, 1.03], # sigma_ij
                [1.03, 1.89]])
    rfr=0
    data = kelley_optimizer( returns, varcov, rfr)
    assert len(data)>0
