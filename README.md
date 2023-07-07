# Fibertree bootstrap code

This Python package provides boilerplate code to intiialize a
[fibertree](https://github.com/Fibertree-Project/fibertree) Python
environment in a Jupyter notebook either in Jupyter lab or Google Colab.


## Demonstration

To see an example of the use of this code in Google Colab click: 
[here](https://colab.research.google.com/github/Fibertree-Project/fibertree-bootstrap/blob/main/notebooks/sample_notebook.ipynb)


## Usage

To use the package put the following in the first cell our your notebook:

```
# Begin - startup boilerplate code

import pkgutil

if 'fibertree_bootstrap' not in [pkg.name for pkg in pkgutil.iter_modules()]:
  !python3 -m pip  install git+https://github.com/Fibertree-Project/fibertree-bootstrap --quiet

# End - startup boilerplate code

from fibertree_bootstrap import *
fibertree_bootstrap(style="tree", animation="movie")
```


