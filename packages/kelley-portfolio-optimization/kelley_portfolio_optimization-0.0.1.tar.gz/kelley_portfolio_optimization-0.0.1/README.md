# Kelley Optimization


## Installation

Run the following to install:

```python
pip install kelley_portfolio_optimization
```

## Usage

```
import numpy as np
returns = np.array([0.0476, 0.004]) # mu
varcov = np.matrix([[2.12, 1.03], # sigma_ij
                [1.03, 1.89]])


```

## Development

To install kelley_portfolio_optimization, along with the tools you need to develop and run tests, run the following in your virtualenv:
```bash
$ pip install -e .[dev]
```
