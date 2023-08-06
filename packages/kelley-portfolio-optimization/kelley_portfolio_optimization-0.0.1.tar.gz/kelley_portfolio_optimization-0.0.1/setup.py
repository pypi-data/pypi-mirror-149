from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author='Christopher Bell',
    author_email='Chris.E.Bell24@gmail.com',
    maintainer='Christopher Bell',
    maintainer_email='Chris.E.Bell24@gmail.com',
    url='https://github.com/chrisebell24/kelley_portfolio_optimization',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    name='kelley_portfolio_optimization',
    version='0.0.1',
    description='Portfolio Optimization',
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['kelley_portfolio_optimization'],
    package_dir={'': 'src'},
    install_requires = [
        "numpy>=1.16.1",
        "pandas>=1.0.0",
        "wget>=3.2",
        "pyomo>=6.3.0",
    ],
    extras_require = {
        "dev": [
            "pytest >= 3.7",
        ],
    },
)
