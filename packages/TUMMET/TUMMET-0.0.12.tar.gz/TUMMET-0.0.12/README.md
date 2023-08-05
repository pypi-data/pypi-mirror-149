

# TUMMET: Analysis and Evaluation for experimental data.
[![PyPI Latest Release](https://img.shields.io/pypi/v/TUMMET?color=blue&style=for-the-badge)](https://pypi.org/project/TUMMET/)

## What is it?

**TUMMET** is a Python package that provides a multitude of functions to quickly analyse, evaluate and visualize experimental material data, while also being easy to use and highly adjustable.

Originally built for the Chair of Metal Structures at the Technical University of Munich [[TUM].](https://www.cee.ed.tum.de/en/metallbau/welcome-page/)

Created and maintained by Michael Winkler -  michael.b.winkler@tum.de

## Current List of Features
Includes: 
- Strain-controlled fatigue test:
  - Reading and evaluating raw data
  - interactive stable zone determination
  - Fitting the Ramberg-Osgood relationship to individual fatigue tests
  - Plotting Hystereses
  - Plotting Cycles-Stress 

- Stress-controlled fatigue test:
    - In Development ... 

- Tensile test:
    - In Development ...

- ...


 



## Where to get it
The source code is currently hosted on GitHub at:
https://github.com/mbwinkler/TUMMET

The latest released version is available through the [Python
Package Index (PyPI)](https://pypi.org/project/TUMMET/).


```sh
pip install TUMMET
```

## Dependencies
- [Pandas](https://pandas.pydata.org/)

- [NumPy](https://www.numpy.org)

- [Matplotlib](https://matplotlib.org/)

- [Seaborn](https://seaborn.pydata.org/)

- [SciPy](https://scipy.org/)

- [tqdm](https://tqdm.github.io/)




## License
[BSD 3](LICENSE)

## Getting Help

For usage questions for a specific function, run the following statement to print the documentation: 
```
help(function_name)
```
