# Fibertree prelude

This Python package provides boilerplate code to intiialize a fibertree
environment in a Jypter notebook either in Jupyter lab or Google Colab.


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


