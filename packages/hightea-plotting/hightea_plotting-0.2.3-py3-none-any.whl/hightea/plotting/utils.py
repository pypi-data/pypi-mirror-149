from .plotting import plot
from .run import Run
import numpy as np


def get_31variation(num,denom):
    """31 scale variation for ratio plot

    Parameters
    ----------
    num : Run
        Run in the numerator.

    denom : Run
        Run in the denomerator.

    Result
    ------
    Run
        Metadata is taken from the numerator.
    """
    setups = [(1,1),(2,2),(0,0),(2,1),(1,2),(0,1),(1,0)]
    variation = [ (i,j) for i in range(7) for j in range(7)
                if not(max(*setups[i],*setups[j]) - min(*setups[i],*setups[j]) == 2) ]
    ratio_runs = [ num[i]/denom[j] for i,j in variation ]
    ratio = Run(bins=num.bins)
    ratio.values = np.transpose([r.v() for r in ratio_runs])
    ratio.errors = np.transpose([r.e() for r in ratio_runs])
    ratio.update_info(num)
    return ratio

